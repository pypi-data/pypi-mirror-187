# pylint: disable=E0611,C0103,R0914,W1514,R1735,R1734,C0206

import asyncio
from typing import Dict, List
from time import time
from zipfile import ZipFile
import tempfile
import json
import os
import shutil
import numpy as np

from ..pytpu import TPUDevice           # type: ignore
from ..pytpu import TPUProgram          # type: ignore
from ..pytpu import TPUInference        # type: ignore
from ..pytpu import TPUProcessingMode   # type: ignore
from ..pytpu import load_inference      # type: ignore
from ..pytpu import get_inference       # type: ignore
from ..pytpu import submit_inference
from ..tools.helpers import to_raw
from ..tools.helpers import STR_TO_DTYPE
from ..tools.helpers import get_tpu_devices

__all__ = [
    'get_fps',
]


async def run_inference(name: str, device: TPUDevice, program: TPUProgram, inference: TPUInference,
                        data_list: List[Dict[str, np.ndarray]]) -> None:

    mode = TPUProcessingMode.kFull.value

    if not bool(program.is_valid()):
        print('\n\nProgram Error: {}\n'.format(program.get_error().decode('utf-8')))

    for ii, data in enumerate(data_list):
        tpu_input, tpu_output, out_ctx = load_inference(data, program)
        inference.set_inputs(tpu_input)
        inference.set_outputs(tpu_output)
        await submit_inference(device, program, inference, tpu_output, mode)
        # data = get_inference(program, tpu_output, out_ctx, as_dict=True, )

        if (ii + 1) % 10 == 0:
            print(f'{name}: finish {ii + 1} iteration')


def get_fps(program_path: str, raw: bool = False, n_queries: int = 100, n_proc: int = 1) -> float:

    print(f'\nStart measure performance for program: {program_path}')
    print(f'\nConfiguration: RAW = {raw}; queries = {n_queries}; processes = {n_proc}')

    tpu_device_names = get_tpu_devices()

    with tempfile.TemporaryDirectory() as tempdir:
        with ZipFile(program_path, 'r') as zip_obj:
            zip_obj.extractall(tempdir)

        with open(os.path.join(tempdir, 'metadata.json'), 'r') as metadata_file:
            metadata = json.load(metadata_file)

        if raw is True:
            with open(os.path.join(tempdir, 'metadata.json'), 'w') as metadata_file:
                metadata = to_raw(metadata)
                json.dump(metadata, metadata_file)

            with tempfile.NamedTemporaryFile() as temp_file:
                program_path = os.path.join(tempdir, 'program_raw.tpu')
                shutil.make_archive(temp_file.name, 'zip', tempdir)
                os.rename(temp_file.name + '.zip', program_path)

            print(f'Raw program saved to {program_path}')

        layers_param = dict()
        for _, region in metadata['inputs'].items():
            for name, inp in region.items():
                layers_param[inp['anchor']] = inp

        data_list = list()
        for _ in range(n_queries):
            for name in layers_param:
                if raw:
                    data_shape = (1, layers_param[name]['size'], )
                    data_type = np.int8
                else:
                    data_shape = layers_param[name]['user_shape']
                    data_type = STR_TO_DTYPE[layers_param[name]['user_dtype']]

                generated_data = (np.random.rand(*data_shape) * 2 - 1) * 100
                generated_data = generated_data.astype(data_type)
                generated_data_dict = {name: generated_data}
                data_list.append(generated_data_dict)

        # input_name = list(layers_param.keys())[0]
        # program_name = os.path.basename(program_path)[:-4]
        # root_dir = os.path.dirname(program_path)
        # with open(os.path.join(root_dir, program_name + '_input.bin'), 'w') as f:
        #     data_list[0][input_name].tofile(f)

        batch = max([layers_param[name]['user_shape'][0] for name in layers_param])

        inference_processes = list()
        device_num = len(tpu_device_names)
        tpu_devices = list()
        tpu_program = TPUProgram(program_path.encode('utf-8'))
        for dev_ii, device_name in enumerate(tpu_device_names):
            tpu_device = TPUDevice(device_name.encode('utf-8'))
            
            if tpu_device.init() < 0:
                raise ConnectionError('Cannot init device')
            
            tpu_device.load_program(tpu_program)
            tpu_devices.append(tpu_device)
            inferences = [TPUInference(tpu_program) for _ in range(n_proc)]
            inference_processes.extend([run_inference(
                name=f'Device {device_name} process {ii}',
                device=tpu_devices[dev_ii],
                program=tpu_program,
                inference=inferences[ii],
                data_list=data_list[ii:len(data_list):n_proc * device_num])
                                        for ii in range(n_proc)])

        start_time = time()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*inference_processes))
        
        total_inference_time = time() - start_time

        fps = n_queries * batch / total_inference_time

        print(f'Estimated FPS = {fps}')

    return fps

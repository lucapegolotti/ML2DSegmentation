# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



# whethre to consider all import modules and perform transformation based on all codes plus all import modules
# Copyright (c) Stanford University, The Regents of the University of
#               California, and others.
#
# All Rights Reserved.
#
# See Copyright-SimVascular.txt for additional details.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
print("imported svWrapper.py")

# if script is launched embedded then
# argv can be unset which throws error
# in tensorflow launch. Setting missing
# argv is a workaround
import sys
if not hasattr(sys, 'argv'):
    sys.argv  = ['']

import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import json

MODEL = "TWO_STREAM"

import torch
from sv_ml.unet import Two_UNet_Fusion
from sv_ml.modules.gvf_image import sv_gvf
from sv_ml.modules import io
from sv_ml.modules import sv_image
from sv_ml.modules import vascular_data

print("importing factories")
# import sv_ml.factories.model_factory as model_factory
import sv_ml.factories.preprocessor_factory as preprocessor_factory
import sv_ml.factories.postprocessor_factory as postprocessor_factory

print("getting directories")
SRC_DIR    = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(SRC_DIR,"config")

# import tensorflow as tf
# tf.set_random_seed(0)

import numpy as np
np.random.seed(0)

class SVWrapper(object):
    def __init__(self, network_type):
        print("SVWrapper init, {}".format(network_type))
        self.cfg_fn = os.path.join(CONFIG_DIR,"{}.yaml".format(network_type))
        print(self.cfg_fn)

        if not os.path.isfile(self.cfg_fn):
            raise RuntimeError("network type does not exist {}".format(self.cfg_fn))

        self.cfg = io.load_yaml(self.cfg_fn)

        p = self.cfg['MODEL_DIR'].replace('./','')
        p = p.split('/')
        self.cfg['MODEL_DIR'] = os.path.join(SRC_DIR,*p)
        if network_type == MODEL:
            self.model_type = network_type
            self.device = 'cpu'
            self.model = Two_UNet_Fusion(n_channels_rgb=1,n_channels_gvf=2, n_classes=1, bilinear=False)
            ckpt = torch.load(self.cfg["MODEL_DIR"],map_location='cpu')
            state = ckpt['state_dict']
            self.model.load_state_dict(state)
        else:
            print("Model dir ", self.cfg['MODEL_DIR'])

            self.model = model_factory.get(self.cfg)

            try:
                self.model.sample()
            except:
                print("using model without sample")

            print("loading model")
            self.model.load()
            print("model loaded")

        self.preprocessor  = preprocessor_factory.get(self.cfg)
        self.postprocessor = postprocessor_factory.get(self.cfg)

    def set_image(self, image_fn):
        # print("setting image {}".format(image_fn))
        if self.model_type == MODEL:
            print("gvf image")
            self.image, self.gvfs = sv_gvf(image_fn)
        else:
            if not os.path.isfile(image_fn):
                raise RuntimeError("image file not found {}".format(image_fn))
            self.image = sv_image.Image(image_fn)
            self.image.set_reslice_ext(self.cfg['CROP_DIMS'])
            self.image.set_spacing(self.cfg['SPACING'])

        return "ok"

    def segment(self, point_string):
        #print("test: point_string {}".format(point_string))
        if self.model_type == MODEL:
            net = self.model.to(self.device)
            net.eval()
            inputs = self.image.to(device=self.device, dtype=torch.float32)
            gvfs = self.gvfs.to(device=self.device, dtype=torch.float32)
            inputs = torch.unsqueeze(inputs,0)
            gvfs = torch.unsqueeze(gvfs,0)
            with torch.set_grad_enabled(False):
                outputs = net(inputs,gvfs)
                pred = (torch.sigmoid(outputs)>0.5).float()
                pred = torch.squeeze(pred)
                pred = torch.squeeze(pred)
                pred =  pred.detach().cpu().numpy()
               
        else:
            try:
                data = json.loads(point_string)
                #print(data)

                p     = data["p"]
                v     = data["n"]
                n     = data["tx"]

                seg = {}

                img = self.image.get_reslice(p,n,v)

                img     = self.preprocessor(img)
                pred    = self.model.predict(img)
                contour = self.postprocessor(pred)

                scale = self.cfg['CROP_DIMS']*self.cfg['SPACING']/2

                # plt.figure()
                # plt.imshow(img[:,:,0],cmap='gray',extent=[-scale,scale,scale,-scale])
                # plt.colorbar()
                # plt.plot(contour[:,0], contour[:,1], color='r', marker='*')
                # plt.savefig('./images/{}.png'.format(seg['index']), dpi=300)
                # plt.close()

                contour[:,1] = contour[:,1]*-1
                contour_3d    = vascular_data.denormalizeContour(contour, p,n,v)
                seg["points"] = contour_3d.tolist()

                return json.dumps(seg)
            except:
                print("error during sv_wrapper.segment")
                return ""

    def sample(self):
        if self.model_type != MODEL:
            self.model.sample()

    def __del__(self):
        if self.model_type != MODEL:
            print("svWrapper destructor")
            self.model.sess.close()
            tf.reset_default_graph()

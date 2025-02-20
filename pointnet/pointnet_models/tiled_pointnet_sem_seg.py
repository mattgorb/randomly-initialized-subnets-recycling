import torch
import torch.nn as nn
import torch.nn.parallel
import torch.utils.data
import torch.nn.functional as F


from pointnet_models.tiled_pointnet_util import TiledPointNetEncoder, TiledSTN3d, TiledSTNkd, feature_transform_reguliarzer, init_conv1d,init_linear

import sys
sys.path.insert(0, '/s/chopin/l/grad/mgorb/parameter_tiling_and_recycling/')
from utils.layer_type import *

class get_tiled_model(nn.Module):
    def __init__(self, num_class, args):
        super(get_tiled_model, self).__init__()
        self.k = num_class
        self.args=args
        self.feat = TiledPointNetEncoder(global_feat=False, feature_transform=True, channel=9, args=self.args)
        self.conv1 = init_conv1d(1088, 512, 1,self.args)
        self.conv2 = init_conv1d(512, 256, 1,self.args)
        self.conv3 = init_conv1d(256, 128, 1,self.args)
        self.conv4 = init_conv1d(128, self.k, 1,self.args)
        self.bn1 = nn.BatchNorm1d(512)
        self.bn2 = nn.BatchNorm1d(256)
        self.bn3 = nn.BatchNorm1d(128)

    def forward(self, x):
        batchsize = x.size()[0]
        n_pts = x.size()[2]
        x, trans, trans_feat = self.feat(x)
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = self.conv4(x)
        x = x.transpose(2,1).contiguous()
        x = F.log_softmax(x.view(-1,self.k), dim=-1)
        x = x.view(batchsize, n_pts, self.k)
        return x, trans_feat

class get_loss(torch.nn.Module):
    def __init__(self, mat_diff_loss_scale=0.001):
        super(get_loss, self).__init__()
        self.mat_diff_loss_scale = mat_diff_loss_scale

    def forward(self, pred, target, trans_feat, weight):
        loss = F.nll_loss(pred, target, weight = weight)
        mat_diff_loss = feature_transform_reguliarzer(trans_feat)
        total_loss = loss + mat_diff_loss * self.mat_diff_loss_scale
        return total_loss


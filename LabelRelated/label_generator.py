
# coding: utf-8

# In[ ]:


import numpy as np


# In[ ]:


class Label_generator:
    def __init__(self,data,wsize=30,mask=None):
        self.fps=data.fps
        #account for slighlty faster framerate due to openface
        self.wsize=wsize
        #self._convert_to_unix_time()
        self.pred_bin=data.get_pred_bin()
        self.mask=mask
        if self.mask is None:
            print('Warning. No filtering mask for bad data points was given. Assuming perfectly clean dataset.')
            self.mask=np.zeros(self.pred_bin.shape[0],dtype='bool')


    #generates labels. Use sliding window if features are also generated with sliding window
    #if a classification method is used, we need a cutoff somewhere :)
    def generate_labels(self,start=0, end=None, sliding_window = 0,method='ratio', classification=False, cutoff=.07):
        if method != 'ratio' and method != 'median':
            raise NameError('The given method does not exist. Try one of the following: ratio,median.')
        if method is 'median':
            print('Note: The median method is currently a 75 percentile.')
        if end is None:
            end = self.pred_bin.shape[0]-1
        if end >= self.pred_bin.shape[0]:
            end = self.pred_bin.shape[0]-1
            print('Desired window too long. Setting end to %ds'% end)
        #average "happiness" per second
        happy_portion = np.nanmean(np.array(self.pred_bin, dtype = 'float'),axis = 1)
        #check nans along the 31FPS
        non_nans_per_s = np.count_nonzero(~np.isnan(np.array(self.pred_bin, dtype='float')),axis = 1)
        #if(sliding_window):
        self.labels = []
        good_ratio = []
        time_it = start
        while True:
            stop = time_it+self.wsize
            curr_mask = np.ma.compressed(np.ma.masked_array(range(time_it,stop),mask=self.mask[time_it:stop]))
            curr_data = happy_portion[curr_mask]           
            curr_non_nans = np.sum(non_nans_per_s[curr_mask])
            if not curr_data.size:
                print('Whole chunk of NaNs. Check this again.')
                if sliding_window:
                    time_it += sliding_window
                else:
                    time_it += self.wsize
                if time_it + self.wsize > end:
                    break
                continue
            #here, we divide by len(curr_data), because we don't want the influence of nans that were thrown away due to bad feature points.
            good_ratio += [float(curr_non_nans)/(self.fps*len(curr_data))]
            if method =='ratio':
                self.labels += [np.nanmean(curr_data)]
            elif method == 'median':
                self.labels += [np.nanpercentile(curr_data,q=75)]
            if sliding_window:
                time_it += sliding_window
            else:
                time_it += self.wsize
            if time_it + self.wsize > end:
                break
        self.labels = np.array(self.labels)

        if(classification):
            #self.labels[np.isnan(self.labels)]=-1
            self.labels[self.labels>cutoff] = 1
            self.labels[(self.labels<1) & (self.labels>-1)] = 0
        return self.labels, good_ratio #THIS IS NOT USED SO FAR, BUT SHOULD BE.


# In[ ]:


# indices=np.array([  161,   162,   163,   173,   174,   175,   176,   177,   178,179,   180,   181,   182,   228,   229,   230,   231,   232,          233,   234,   235,   236,   259,   260,   261,   262,   263,          264,   265,   266,   267,   268,   269,   270,   271,   272,          273,   274,   275,   276,   277,   278,   279,   280,   281,          282,   283,  1284,  1285,  1286,  1287,  1288,  1289,  1290,         1291,  1472,  1473,  1474,  1475,  1907,  1908,  1909,  1910,         2150,  2151,  2152,  2153,  2154,  2409,  2410,  2411,  2412,
#          2413,  2414,  2415,  2416,  2417,  2418,  2419,  2420,  2780,         2781,  2782,  2997,  2998,  2999,  3000,  3001,  3002,  3003,         3004,  3005,  3029,  3030,  3031,  3032,  3033,  3034,  3035,         3036,  3037,  3443,  3444,  3445,  3451,  3452,  3453,  3486,         3487,  3488,  3489,  3490,  3491,  3492,  3493,  3494,  3651,         3652,  3653,  3654,  3655,  3656,  3657,  3658,  3659,  3688,         3689,  3690,  3691,  3692,  3693,  3694,  3710,  3711,  3712,         3713,  3714,  3715,  3716,  3717,  3718,  3719,  3720,  3729,
#          3730,  3731,  3732,  3733,  3734,  3735,  3736,  3737,  3738,         3739,  3740,  3741,  3742,  3743,  3744,  3745,  3746,  3747,         3748,  3749,  3751,  3752,  3753,  3754,  4280,  4281,  4282,         4283,  4284,  4285,  4286,  4287,  8187,  8188,  8189,  8190,         8191,  8192,  8193,  8194, 12643, 12644, 12645, 12646, 12647,        12661, 12662, 12663, 12664, 22924, 22925, 22926, 22956, 22957,        22958, 22969, 22970, 22971, 22999, 23000, 23001, 23003, 23004,        23005, 27302, 27303, 27304, 28218, 28219, 28220, 29225, 29226,
#         29227, 29228, 29229, 29230, 29231, 29232, 29233, 29234, 29235,        29236, 29237, 29238, 29239, 29240, 29241, 29242, 29243, 29244,        29245, 29246, 29247, 29248, 29271, 29272, 29273, 29274, 29275,        29276, 29277, 29278, 29279, 29280, 29281, 29282, 29283, 29284,        29285, 29286, 29287, 29288, 29289, 29290, 29291, 29292, 29293,        29294, 29295, 29296, 29297, 29298, 29299, 29300, 29301, 29302,        29303, 29304, 29305, 29306, 29307, 29308, 29309, 29310, 29311,        29312, 29313, 29314, 29315, 29316, 29317, 29318, 29319, 29320,
#         29321, 29322, 29323, 29324, 29325, 29326, 29327, 29328, 29329,        29330, 29331, 29332, 29333, 29334, 29335, 29336, 29337, 29338,        29339, 29340, 29341, 29342, 29343, 29344, 29345, 29346, 29347,        29348, 29349, 29350, 29351, 29352, 29382, 29383, 29384, 29385,        29386, 29387, 29388, 29389, 29390, 29391, 29392, 29393, 29394,        29395, 29396, 29397, 29398, 29399, 29400, 29401, 29402, 29403,        29404, 29405, 29406, 29407, 29408, 29409, 29410, 29411, 29494,        29495, 29496, 29502, 29503, 29504, 29505, 29506, 29507, 29508,
#         29509, 29510, 29511, 29512, 29513, 29514, 35518, 35519, 35520,        35696, 35697, 35698, 35861, 35862, 35863, 36151, 36152, 36153,        36154, 36155, 36156, 36157, 36158, 36159, 36160, 36161, 36162,        36163, 36164, 36165, 36166, 36297, 36298, 36299, 37687, 37688, 37689])
# mask=np.zeros(45000)
# mask[indices]=1


# In[ ]:


# stop=12500
# start=11
# test=Label_generator('/home/emil/data/hdf_data/cb46fd46_8_imp_columns.hdf', start=start,stop=stop, wsize=100)
# meds,meds_rat=test.generate_labels(method='median',mask=mask)
# mea,mea_rat=test.generate_labels(method='ratio',mask=mask)
# meds_sl, meds_sl_rat=test.generate_labels(method='median', sliding_window=True,mask=mask)
# mea_sl,mea_sl_rat=test.generate_labels(method='ratio',sliding_window=True,mask=mask)

# meds_cl, meds_cl_rat=test.generate_labels(method='median', classification=True, cutoff=.1,mask=mask)
# mea_cl, mea_cl_rat=test.generate_labels(method='ratio',classification=True,cutoff=.1,mask=mask)


# In[ ]:


#import matplotlib.pyplot as plt
# #plot the nan ratio
# br=np.unique(np.array(test.pred_bin, dtype='float'), return_counts=True)
# sum_nans=np.sum(br[1][2:])
# #print(sum_nans)
# vals=([str(br[0][0]),str(br[0][1]),str(br[0][2])],[br[1][0],br[1][1],sum_nans])
# print(vals[0],vals[1])
# plt.bar(vals[0],vals[1])
# plt.title("Occurences of 'Happy'/'Not Happy'/'N/A' predictions in %ds of data" % (stop-start))
# plt.xlabel('Prediction')
# plt.ylabel('Occurences')


# In[ ]:


# #plot stuff
# plt.scatter(range(len(mea)),mea, c=mea_rat)
# plt.plot(range(len(mea)),mea, 'y--')
# plt.title('Mean Happiness, windowsize %ds' %test.wsize)
# plt.ylabel('Value')
# plt.xlabel('Data point no.')
# cbar=plt.colorbar()
# cbar.set_label('Ratio Pred:NaN')
# plt.show()

# plt.scatter(range(len(meds)),meds, c=meds_rat)
# plt.plot(meds, 'y--')
# cbar=plt.colorbar()
# cbar.set_label('Ratio Pred:NaN')
# plt.title('25th Percentile Happiness, windowsize %ds' %test.wsize)
# plt.ylabel('Value')
# plt.xlabel('Data point no.')
# plt.show()

# plt.scatter(range(len(meds_sl)),meds_sl, c=meds_sl_rat)
# #plt.plot(meds_sl, 'b--')
# plt.ylabel('Value')
# plt.xlabel('Data point no.')
# plt.title('25th Percentile Happiness, sliding window of %ds' %test.wsize)
# cbar=plt.colorbar()
# cbar.set_label('Ratio Pred:NaN')
# plt.show()

# plt.scatter(range(len(mea_sl)),mea_sl, c=mea_sl_rat)
# #plt.plot(mea_sl, label='Mean')
# plt.ylabel('Value')
# plt.xlabel('Data point no.')
# plt.title('Mean Happiness, sliding window of %ds' %test.wsize)
# plt.legend()
# cbar=plt.colorbar()
# cbar.set_label('Ratio Pred:NaN')
# plt.show()

# plt.plot(mea_cl,'b.', label='Mean',)
# plt.ylabel('Value')
# plt.xlabel('Data point no.')
# plt.title('Mean and classification method, windowsize of %ds, threshold of %2.2f' % (test.wsize,.16))
# plt.legend()
# plt.show()

# plt.plot(meds_cl,'b.', label='Median',)
# plt.ylabel('Value')
# plt.xlabel('Data point no.')
# plt.title('25th Percentile and classification method, windowsize of %ds, threshold of %2.2f' % (test.wsize,.16))
# plt.show()


# In[ ]:


# plt.scatter(range(1400),test.df['Happy_predicted'].values[:1400], s=2)
# plt.title('Raw HappyFace Predictions')
# plt.xlabel('t')
# plt.ylabel('Happy (binary)')


# In[ ]:


#test=Label_generator('/home/emil/data/hdf_data/cb46fd46_8_imp_columns.hdf',start=11,stop=43205)

# mas=test.generate_labels(start=0, end=30000,method='ratio',mask=None)

# # plt.plot(np.mean(test.pred_bin,axis=0))
# # plt.xlabel('sec')
# # plt.ylabel('Happy prediction')


# # plt.plot(test.labels)
# # plt.xlabel('window')
# plt.ylabel('Happy prediction')


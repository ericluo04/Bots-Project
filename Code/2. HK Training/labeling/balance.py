import pandas as pd

data = pd.read_csv('Data/labeled_tweets.csv', index_col = 0)
data.columns = ['tweet', 'label']
# dropping all rows with duplicate tweets
data.drop_duplicates(subset = "tweet", keep = False, inplace = True) 

#see how many are in each group
anti = data.label.sum()
pro = data.shape[0] - data.label.sum()

print('Anti: percentage : ', anti/data.shape[0], ' number :', anti)
print('Pro: percentage : ', pro/data.shape[0], ' number :', pro)

if anti < pro:
		maj = 0
		min_ = 1
		party_min = 'anti'
else:
	maj = 1
	min_ = 0
	party_min = 'pro'

def downsample(data, anti, pro, maj, min_, party_min):
	'''
	takes original dataset and downsample it
	output a smaller dataset
	'''
	majority = data[data.label == maj].sample(min(anti, pro))
	minority = data[data.label == min_]
	#concatenate the two 
	data = pd.concat([majority, minority], axis = 0)
	print('after balancing the data:')
	anti = data.label.sum()
	pro = data.shape[0] - data.label.sum()
	print('Anti: percentage : ', anti/data.shape[0], ' number :', anti)
	print('Pro: percentage : ', pro/data.shape[0], ' number :', pro)
	data.to_csv('Data/labeled_data_balanced.csv')
	return(data)


def increase(data, anti, pro, maj, min_, party_min): 
	'''
	takes as input the minority party and increases your original dataset 
	'''
	from label import get_data
	int_files = [] #Warning do not include previous files used for original dataset. You'll end up iwth duplicates
	n_max = max(anti, pro) #as we want to match it 
	get_data(int_files, n_max, party = party_min)


#choose which method you want to use 
#WARNING: the increase method directly increases the data to your oiriginal dataset. 
#increase()

downsample(data, anti, pro, maj, min_, party_min)







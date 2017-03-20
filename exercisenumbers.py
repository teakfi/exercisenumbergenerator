#!/usr/bin/python3

import random
import sys
import argparse

class RndGeneratorFactory(object):
	class Distribution:
		def StepSize(self,oddness, min_value):
			step=1
	
			if oddness=='odd':
				if not min_value%2:
					min_value=min_value+1

				step=2
				
			elif oddness=='even':
				if min_value%2:
					min_value=min_value+1
				
				step=2		
				
			return [step,min_value]
						
	class AllValuesDistribution(Distribution):
		def CalcValues(self,min_value, max_value, oddness,how_many_values):
			[step,min_value]=super().StepSize(oddness,min_value)
			values=list(range(min_value,max_value+1,step))
			return values
		
		
	class FlatRndDistribution(Distribution):

		def CalcValues(self,min_value,max_value,oddness,how_many_values):
			count=0
			[step,min_value]=super().StepSize(oddness,min_value)
			values=[]
			while count < how_many_values:
				number=random.randrange(min_value,max_value+1,step)
				if not number in values:
					values.append(number)
					count=count+1
			return values
			

		@staticmethod	
		def ArgumentListing():
			return ['--flat', 'flat',0,True,'Flat distribution, default']

		
	class GaussRndDistribution(Distribution):
		def CalcValues(self,min_value,max_value,oddness,mean,sigma,how_many_values):
			count=0
			values=[]
			while count < how_many_values:
				number=int(random.gauss(mean,sigma))
				if oddness=='odd' and not number%2:
					continue
		
				if oddness=='even' and  number%2:
					continue
		
				if number>=min_value and number<=max_value and not number in values:
					values.append(number)
					count=count+1
			return values
		
		
	class LowGaussRndDistribution(GaussRndDistribution):
		def CalcValues(self,min_value,max_value,oddness,how_many_values):
			sigma=(min_value+max_value)/4
			mean=min_value
			values=super().CalcValues(min_value,max_value,oddness,mean,sigma,how_many_values)
			return values
		
		@staticmethod
		def ArgumentListing():
			return ['--low','low',1,False,'Gaussian distribution, low values prefered, mean = min value, sigma = (min + max) / 4']
		
	class HighGaussRndDistribution(GaussRndDistribution):
		def CalcValues(self,min_value,max_value,oddness,how_many_values):
			sigma=(min_value+max_value)/4
			mean=max_value
			values=super().CalcValues(min_value,max_value,oddness,mean,sigma,how_many_values)
			return values

		@staticmethod
		def ArgumentListing():
			return ['--high','high',2,False,'Gaussian distribution, high values prefered, mean = max value, sigma = (min + max) / 4']
		
	class CentralGaussRndDistribution(GaussRndDistribution):
		def CalcValues(self,min_value,max_value,oddness,how_many_values):
			sigma=(min_value+max_value)/4
			mean=sigma*2
			values=super().CalcValues(min_value,max_value,oddness,mean,sigma,how_many_values)
			return values
		

		@staticmethod
		def ArgumentListing():
			return ['--central','central',3,False,'Gaussian distribution, mean = (min+max)/2, sigma = (min + max) / 4']

	@staticmethod
	def Factory(distribution):
		random.seed()
		if distribution == "all": return RndGeneratorFactory.AllValuesDistribution()
		if distribution == "flat": return RndGeneratorFactory.FlatRndDistribution()
		if distribution == "central": return RndGeneratorFactory.CentralGaussRndDistribution()
		if distribution == "low": return RndGeneratorFactory.LowGaussRndDistribution()
		if distribution == "high": return RndGeneratorFactory.HighGaussRndDistribution()
		assert 0, "Undefined distribution: " + distribution
		
	@staticmethod
	def ListDistributionArguments():
		return [ \
			RndGeneratorFactory.FlatRndDistribution.ArgumentListing(), \
			RndGeneratorFactory.LowGaussRndDistribution.ArgumentListing(), \
			RndGeneratorFactory.CentralGaussRndDistribution.ArgumentListing(), \
			RndGeneratorFactory.HighGaussRndDistribution.ArgumentListing() \
			]

            

class TextUI():
	def Calculate(self,min_value, max_value, how_many_values, only_odd, only_even, chosen):

		oddness='none'
		if only_odd:
			oddness='odd'
		if only_even:
			oddness='even'	

		number_of_poss_values=(max_value-min_value)
		if oddness!='none':
			number_of_poss_values=number_of_poss_values/2

		if how_many_values>=number_of_poss_values:
			chosen='all'



		RndGenerator=RndGeneratorFactory.Factory(chosen)
		values=RndGenerator.CalcValues(min_value,max_value,oddness,how_many_values)
		values.sort()
		print(values)
		return;


def main():
	descStr="""
	This program generates list of numbers with minimum, and maximum values, possibility to choose only odd or even numbers, using desired distribution
	"""

	DistributionArguments=RndGeneratorFactory.ListDistributionArguments()
	parser = argparse.ArgumentParser(description=descStr)
	parity = parser.add_mutually_exclusive_group()
	parity.add_argument('--odd', action='store_true', default=False, help='give only odd values')
	parity.add_argument('--even', action='store_true', default=False, help='give only even values')
	parser.add_argument('minv', metavar='MIN', type=int, help='minimum value')
	parser.add_argument('maxv', metavar='MAX', type=int, help='maximum value')
	parser.add_argument('number', metavar='needed', type=int, help='how many values are needed')
	distribution=parser.add_mutually_exclusive_group()
	for dists in DistributionArguments:
		if dists[3]==True:
			distribution.add_argument(dists[0],action='store_const',dest='chosen_dist',const=dists[2],default=dists[2],help=dists[4])
		else:
			distribution.add_argument(dists[0],action='store_const',dest='chosen_dist',const=dists[2],help=dists[4])
	

	args=parser.parse_args()

	for dists in DistributionArguments:
		if args.chosen_dist==dists[2]:
			chosen_dist=dists[1]
			break
				
	UI=TextUI()
	UI.Calculate(args.minv,args.maxv,args.number, args.odd, args.even, chosen_dist)
	

	return 0

if __name__=='__main__':
	main()

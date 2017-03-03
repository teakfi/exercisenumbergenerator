import random
import sys
import argparse


def calcvalues( min_value, max_value, how_many_values, only_odd, only_even, chosen_distribution ):
    step=1
    if only_odd and only_even:
        sys.exit()

    elif only_odd:
        if not min_value%2:
            min_value=min_value+1

        step=2
            
    elif only_even:
        if min_value%2:
            min_value=min_value+1
                
        step=2

    if how_many_values>(max_value-min_value)/step:
        values=range(min_value,max_value,step)
        print(values)
        sys.exit()
    
    values = []


    distributions=['flat','central gauss','low gauss','high gauss']
    if not chosen_distribution < len(distributions):
        sys.exit()
    if chosen_distribution < 0:
        sys.exit()

    chosen=distributions[chosen_distribution]

    random.seed()
    count = 0
    if chosen == 'flat':
        while count < how_many_values:
            number=random.randrange(min_value,max_value,step)
            if not number in values:
                values.append(number)
                count=count+1

            
    else:
        sigma=(min_value+max_value)/4
        if chosen =='central gauss':
            mean=sigma*2
        elif chosen=='low gauss':
            mean=min_value
        elif chosen=='high gauss':
            mean=max_value

        while count < how_many_values:
            number=int(random.gauss(mean,sigma))
            if only_odd and not number%2:
                continue

            if only_even and  number%2:
                continue
        
            if number>=min_value and number<=max_value and not number in values:
                values.append(number)
                count=count+1

            
    values.sort()
    print(values)
    return;


def main():
    descStr="""
    This program generates list of numbers with minimum, and maximum values, possibility to choose only odd or even numbers, using desired distribution
    """

    only_odd=False
    only_even=False
    parser = argparse.ArgumentParser(description=descStr)
    parity = parser.add_mutually_exclusive_group()
    parity.add_argument('--odd', action='store_true')
    parity.add_argument('--even', action='store_true')
    parser.add_argument('minv', metavar='MIN', type=int, help='minimum value')
    parser.add_argument('maxv', metavar='MAX', type=int, help='maximum value')
    parser.add_argument('number', metavar='X', type=int, help='how many values')
    distribution=parser.add_mutually_exclusive_group()
    distribution.add_argument('--flat', dest='chosen_dist',action='store_const', const=0, default=0, help='flat distribution, default one')
    distribution.add_argument('--central', dest='chosen_dist', action='store_const', const=1, help='central gaussian distribution')
    distribution.add_argument('--low', dest='chosen_dist',action='store_const', const=2, help='low gaussian distribution')
    distribution.add_argument('--high', dest='chosen_dist', action='store_const', const=3, help='high gaussian dsitribution')

    args=parser.parse_args()
    
    calcvalues(args.minv,args.maxv,args.number, args.odd, args.even, args.chosen_dist)


    return 0

if __name__=='__main__':
    main()

import numpy as np
import pandas as pd
from scipy import stats


def balanceCheckTtest(label, divisor, sampleDF, populationDF):
    sample_mean = np.nanmean(sampleDF[label])/divisor
    population_mean = np.nanmean(populationDF[label])/divisor
    difference = sample_mean-population_mean
    p_value = stats.ttest_1samp(sampleDF[label].values/divisor, population_mean, nan_policy='omit')[1]
    
    return round(sample_mean,2), round(population_mean,2), round(difference,2), round(p_value,2)



def balanceCheckChiSquare(label, value, sampleDF, populationDF):
    sample_mean = sum(sampleDF[label] == value)/len(sampleDF)
    population_mean = sum(populationDF[label] == value)/len(populationDF)
    difference = sample_mean-population_mean
    p_value = stats.chisquare(
        [sample_mean, 1-sample_mean],
        [population_mean, 1-population_mean]
    )[1]
    
    return round(sample_mean,2), round(population_mean,2), round(difference,2), round(p_value,2)



def balanceCheckMultiple(rows, outDF, sample, all_firms):
    for row in rows:
        if row['test'] == 'ttest':
            outDF.loc[row['name']] = balanceCheckTtest(label=row['attrs'][0], divisor=row['attrs'][1], sampleDF=sample, populationDF=all_firms)
        elif row['test'] == 'chisquare':
            outDF.loc[row['name']] = balanceCheckChiSquare(label=row['attrs'][0], value=row['attrs'][1], sampleDF=sample, populationDF=all_firms)
    outDF.loc['n'] = [len(sample), len(all_firms), '-', '-']
    return outDF
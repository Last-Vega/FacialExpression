# 以下が，DawidとSkeneのモデルのコードになります．
# 主に修正する必要があると思われるのは，データファイルの入力部分だと思います．

### import
import csv
import numpy as np
import sys
import os


"""
Function: em()
    Run the EM estimator on the data from the Dawid-Skene paper
"""
### em
def em(responses):
    # run EM
    sample_classes, error_rates, samples, observers, classes = run(responses)

    return sample_classes, error_rates, samples, observers, classes

"""
Function: dawid_skene()
    Run the Dawid-Skene estimator on response data
Input:
    responses: a dictionary object of responses:
        {patients: {observers: [labels]}}
    tol: tolerance required for convergence of EM
    max_iter: maximum number of iterations of EM
"""
### run
def run(responses, tol=0.00001, max_iter=100, init='average'):
    # convert responses to counts
    (samples, observers, classes, counts) = responses_to_counts(responses)
    print("num samples:", len(samples))
    print("Observers:", observers)
    print("Classes:", classes)

    # initialize
    iter = 0
    converged = False
    old_class_marginals = None
    old_error_rates = None
    sample_classes = initialize(counts)
    print("Iter\tlog-likelihood\tdelta-CM\tdelta-ER")

    # while not converged do:
    while not converged:
        iter += 1

        # M-step
        (class_marginals, error_rates) = m_step(counts, sample_classes)

        # E-setp
        sample_classes = e_step(counts, class_marginals, error_rates)

        # check likelihood
        log_L = calc_likelihood(counts, class_marginals, error_rates)

        # check for convergence
        if old_class_marginals is not None:
            class_marginals_diff = np.sum(np.abs(class_marginals - old_class_marginals))
            error_rates_diff = np.sum(np.abs(error_rates - old_error_rates))
            print(iter, '\t', log_L, '\t%.6f\t%.6f' % (class_marginals_diff, error_rates_diff))
            if (class_marginals_diff < tol and error_rates_diff < tol) or iter > max_iter:
                converged = True
        else:
            print(iter, '\t', log_L)

        # update current values
        old_class_marginals = class_marginals
        old_error_rates = error_rates

    # Print final results
    np.set_printoptions(precision=2, suppress=True)
    print("Class marginals")
    print(class_marginals)
    print("Error rates")
    print(error_rates)
    print("Sample classes")
    print(sample_classes)
    #print("Incidence-of-error rates")
    #[nsamples, nObservers, nClasses] = np.shape(counts)
    #for k in range(nObservers):
    #    print(class_marginals * error_rates[k,:,:])
    #np.set_printoptions(precision=4, suppress=True)

    return sample_classes, error_rates, samples, observers, classes

"""
Function: responses_to_counts()
    Convert a matrix of annotations to count data
Inputs:
    responses: dictionary of responses {patient:{observers:[responses]}}
Return:
    patients: list of patients
    observers: list of observers
    classes: list of possible patient classes
    counts: 3d array of counts: [patients x observers x classes]
"""
### responses to counts
def responses_to_counts(responses):
    samples = list(responses)
    sorted(samples)
    nsamples = len(samples)

    # determine the observers and classes
    observers = set()
    classes = set()
    for i in samples:
        i_observers = list(responses[i])
        for k in i_observers:
            if k not in observers:
                observers.add(k)
            ik_responses = responses[i][k]
            classes.update(ik_responses)

    classes = list(classes)
    sorted(classes)
    nClasses = len(classes)

    observers = list(observers)
    observers.sort()
    nObservers = len(observers)

    # create a 3d array to hold counts
    counts = np.zeros([nsamples, nObservers, nClasses])

    # convert responses to counts
    for sample in samples:
        i = samples.index(sample)
        for observer in list(responses[sample]):
            k = observers.index(observer)
            for response in responses[sample][observer]:
                j = classes.index(response)
                counts[i,k,j] += 1

    return (samples, observers, classes, counts)

"""
Function: initialize()
    Get initial estimates for the true patient classes using counts
    see equation 3.1 in Dawid-Skene (1979)
Input:
    counts: counts of the number of times each response was received
        by each observer from each patient: [patients x observers x classes]
Returns:
    patient_classes: matrix of estimates of true patient classes:
        [patients x responses]
"""
### initialize
def initialize(counts):
    [nsamples, nObservers, nClasses] = np.shape(counts)
    # sum over observers
    response_sums = np.sum(counts,1)
    # create an empty array
    sample_classes = np.zeros([nsamples, nClasses])
    # for each sample, take the average number of observations in each class
    for p in range(nsamples):
        sample_classes[p,:] = response_sums[p,:] / np.sum(response_sums[p,:],dtype=float)

    return sample_classes

"""
Function: m_step()
    Get estimates for the prior class probabilities (p_j) and the error
    rates (pi_jkl) using MLE with current estimates of true patient classes
    See equations 2.3 and 2.4 in Dawid-Skene (1979)
Input:
    counts: Array of how many times each response was received
        by each observer from each patient
    patient_classes: Matrix of current assignments of patients to classes
Returns:
    p_j: class marginals [classes]
    pi_kjl: error rates - the probability of observer k receiving
        response l from a patient in class j [observers, classes, classes]
"""
### M-step
def m_step(counts, sample_classes):
    [nsamples, nObservers, nClasses] = np.shape(counts)

    # compute class marginals
    class_marginals = np.sum(sample_classes,0) / float(nsamples)

    # compute error rates
    error_rates = np.zeros([nObservers, nClasses, nClasses])
    for k in range(nObservers):
        for j in range(nClasses):
            for l in range(nClasses):
                error_rates[k, j, l] = np.dot(sample_classes[:,j], counts[:,k,l])
            # normalize by summing over all observation classes
            sum_over_responses = np.sum(error_rates[k,j,:])
            if sum_over_responses > 0:
                error_rates[k,j,:] = error_rates[k,j,:] / float(sum_over_responses)

    return (class_marginals, error_rates)

"""
Function: e_step()
    Determine the probability of each patient belonging to each class,
    given current ML estimates of the parameters from the M-step
    See equation 2.5 in Dawid-Skene (1979)
Inputs:
    counts: Array of how many times each response was received
        by each observer from each patient
    class_marginals: probability of a random patient belonging to each class
    error_rates: probability of observer k assigning a patient in class j
        to class l [observers, classes, classes]
Returns:
    patient_classes: Soft assignments of patients to classes
        [patients x classes]
"""
### E-step
def e_step(counts, class_marginals, error_rates):
    [nsamples, nObservers, nClasses] = np.shape(counts)
    sample_classes = np.zeros([nsamples, nClasses])

    for i in range(nsamples):
        for j in range(nClasses):
            estimate = class_marginals[j]
            estimate *= np.prod(np.power(error_rates[:,j,:], counts[i,:,:]))

            sample_classes[i,j] = estimate
        # normalize error rates by dividing by the sum over all observation classes
        sample_sum = np.sum(sample_classes[i,:])
        if sample_sum > 0:
            sample_classes[i,:] = sample_classes[i,:] / float(sample_sum)

    return sample_classes

"""
Function: calc_likelihood()
    Calculate the likelihood given the current parameter estimates
    This should go up monotonically as EM proceeds
    See equation 2.7 in Dawid-Skene (1979)
Inputs:
    counts: Array of how many times each response was received
        by each observer from each patient
    class_marginals: probability of a random patient belonging to each class
    error_rates: probability of observer k assigning a patient in class j
        to class l [observers, classes, classes]
Returns:
    Likelihood given current parameter estimates
"""
### calculate likelihood
def calc_likelihood(counts, class_marginals, error_rates):
    [nsamples, nObservers, nClasses] = np.shape(counts)
    log_L = 0.0

    for i in range(nsamples):

        sample_likelihood = 0.0

        for j in range(nClasses):
            class_prior = class_marginals[j]
            sample_class_likelihood = np.prod(np.power(error_rates[:,j,:], counts[i,:,:]))
            sample_class_posterior = class_prior * sample_class_likelihood
            sample_likelihood += sample_class_posterior
        temp = log_L + np.log(sample_likelihood)

        if np.isnan(temp) or np.isinf(temp):
            print(i, log_L, np.log(sample_likelihood), temp)
            sys.exit()

        log_L = temp

    return log_L

### データを入力する．
def input_data():
    # 入力するデータファイルを取得
    filename = sys.argv[1]

    responses = {}
    # responsesの中身は，以下のようにようになっています．
    # responses = {TaskID : {WorkerID : [answer], WorkerID : [answer], ........},
    #              TaskID : {WorkerID : [answer], WorkerID : [answer], ........},
    #             }

    # データファイルを読み込み，辞書responsesの作成
    # データファイルのフォーマットが異なる場合はここを修正してください．responsesの中身が上で示すように作るのがいいと思います．
    with open(filename, newline="") as f:
        reader = csv.reader(f, delimiter="\t", quotechar='"')
        h = next(csv.reader(f))
        for row in reader:
            if row[0] in responses.keys():
                responses[row[0]][row[1]] = [row[2]]
            else:
                responses[row[0]] = {}
                responses[row[0]][row[1]] = [row[2]]

    return responses, filename

### ファイルを出力する．
def write_file(sample_classes, error_rates, samples, observers, classes, filename):
    answer_labels = np.argmax(sample_classes, axis = 1) # 各タスクの確率が最大のクラス(index)を取得します．
    estimate_labels = []
    for answer in answer_labels:
        estimate_labels.append(classes[answer])

    # 各タスクの推定されたラベルを出力する．
    # 異なるフォーマットのファイルを出力させたい場合は，ここを修正してください．
    class_file = 'class_' + filename
    with open(class_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['TaskID', 'Estimate_label']) # header
        for num in range(len(samples)):
            writer.writerow([samples[num], estimate_labels[num]])


    # 各ワーカの推定された能力を出力する．
    # 異なるフォーマットのファイルを出力させたい場合は，ここを修正してください．
    error_file = 'error_' + filename
    with open(error_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # header
        header = ['WorkerID']
        for j in classes:
            for l in classes:
                header.append(j+'_'+l)
        writer.writerow(header)

        for k in range(len(observers)):
            row = []
            row.append(observers[k])
            for j in range(len(classes)):
                for l in range(len(classes)):
                    row.append(error_rates[k,j,l])
            writer.writerow(row)

### main
def main():
    responses, filename = input_data() # データの入力
    sample_classes, error_rates, samples, observers, classes = em(responses) # DawidとSkeneのモデル(EMアルゴリズム)
    write_file(sample_classes, error_rates, samples, observers, classes, filename) # ファイルを出力

if __name__ == '__main__':
    main() 

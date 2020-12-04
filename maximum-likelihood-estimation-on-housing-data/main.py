import numpy as np
import pandas as pd
from functools import reduce
from dateutil import parser as date_parser
import matplotlib.pyplot as plt
import funcy as fnc
import argparse
import pickle as pk
import os
from pathlib import Path

plt.style.use(['ggplot'])


def minus(l, pred):
    return list(filter(pred, l))

def split_date(df):
    col_name = 'date'
    df[col_name] = [date_parser.parse(d) for d in df[col_name]]
    df['day'] = [d.day for d in df[col_name]]
    df['month'] = [d.month for d in df[col_name]]
    df['year'] = [d.year for d in df[col_name]]
    df['weekday'] = [d.isoweekday() for d in df[col_name]]
    df = df.drop(col_name, axis=1)
    return df


def getWeights(include_cols, dfs):
    x = reduce(lambda l1, l2: l1.append(l2), list(map(lambda d: d[include_cols], dfs)))
    return dict(map(lambda i: [i, ((x[i].max(), x[i].min()))], include_cols))


def normalize(wts, df):
    for i in wts.keys():
        df[i] = df[i].apply(lambda z: ((z - wts[i][1]) / (wts[i][0] - wts[i][1])))
    return df


def calc_cost(theta, X, y):
    return (np.sum(np.square(X.dot(theta) - y)))


def gradient_descent(td, vd, theta, learning_rate=0.0001, iterations=30000, lmbda=0):
    X, y = td
    X_v, y_v = vd
    cost_history = list()
    theta_history = list()
    gradient_history = list()
    validation_history = list()
    raw_theta_history = list()
    for it in range(iterations):
        y_hat = np.dot(X, theta)
        cost_gradient = X.T.dot((y_hat - y))
        reg_gradient = lmbda * np.concatenate((np.array([0]).reshape(1, 1), theta[1:]), axis=0)
        gradient = cost_gradient + reg_gradient
        theta = theta - learning_rate * (gradient)

        if (it % 100 == 0):
            print("iteration:", it)
            print("cost:", calc_cost(theta, X, y), "gradient", np.linalg.norm(gradient), "theta", np.linalg.norm(theta),
                  "learning rate = ", learning_rate, "lambda", lmbda)

        raw_theta_history.append(theta)
        theta_history.append(np.linalg.norm(theta))
        cost_history.append(calc_cost(theta, X, y))
        validation_history.append(calc_cost(theta, X_v, y_v))
        gradient_history.append(np.linalg.norm(gradient))

        if (np.linalg.norm(gradient) < 0.5):
            print('COVERGENCE ACHIEVED !!!! iteration : ', it)
            break;
        if (np.linalg.norm(gradient) > 100000000000):
            print('CANNOT CONVERGE !!!! ')
            break;

    return theta, cost_history, theta_history, gradient_history, validation_history, raw_theta_history


def getCorrelationMatrix(df):
    import seaborn as sns
    plt.gcf().clear()
    f, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr().sort_values(by=['price'], ascending=False)
    # print(df.corr())
    snsplot = sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),
                          cmap=sns.diverging_palette(220, 10, as_cmap=True),
                          square=True, ax=ax)
    snsFig = snsplot.get_figure()
    snsFig.savefig("CorrelationMatrix.png")


def plotGradientDescent(cost_history, gradient_history, validation_history, theta, theta_history, name_pre, lr,
                        lmbd=0):
    f = {'size': 6}
    import matplotlib.pyplot as plt
    plt.plot(cost_history, label='Cost History')
    plt.plot(gradient_history, label='Gradient History')
    plt.plot(validation_history, label='Validation History')
    print("norm of theta", np.linalg.norm(theta))
    print('Final SSE for training data {:0.3f}'.format(cost_history[-1]))
    print('Final SSE for Validation data {:0.3f}'.format(validation_history[-1]))
    print('')
    plt.yscale('log')
    plt.title("Theta" + str(theta_history[-1]) + "\n TLoss" + str(cost_history[-1]) + "\nVLoss"
              + str(validation_history[-1]) + "\nGrad" + str(gradient_history[-1]), fontdict=f)
    plt.legend()
    plt.savefig(Path("results", "plots", name_pre + "_" + str(lr) + "_" + str(lmbd) + ".png"))
    plt.gcf().clear()





if __name__ == "__main__":
    if not os.path.exists('results'): os.makedirs('results')
    if not os.path.exists(Path('results', "plots")):
        os.makedirs(Path('results', "plots"))

    parser = argparse.ArgumentParser(description="argparse for different lambdas")
    parser.add_argument("-cm","--get_corr_matrix", action="store_true", help="set to get correlation matrix")
    parser.add_argument("-lr","--learning_rate", type= float, default=0.00005, help="set learning rate")
    parser.add_argument("-itr","--iterations", type= int, default=1000, help="set learning iterations")

    args = parser.parse_args()



    ####################### Load Data #######################################################################
    data = [pd.read_csv(Path("seed_data","PA1_train.csv")),
        pd.read_csv(Path("seed_data","PA1_dev.csv")),
        pd.read_csv(Path("seed_data","PA1_test.csv"))]


    if args.get_corr_matrix:
        getCorrelationMatrix(data[0])


    ##################################### Data preprocessing ################################################
    # PART 0
    # (a)
    removeId = lambda df: df.drop('id', axis=1)
    removeDummy = lambda df: df.drop('dummy', axis=1)

    # (b)
    splitDate = lambda df: split_date(df)
    data = list(map(lambda df: split_date(df), data))

    # (e)
    normaliseCols = data[0].drop(['price', 'dummy', 'id'], axis=1).columns
    nrmlz = fnc.partial(normalize, getWeights(normaliseCols, data))
    clean_data = [nrmlz(removeDummy(removeId(d))) for d in data]
    clean_train_df, clean_dev_df, clean_test_df = clean_data

    # (c)
    stats = clean_train_df[minus(clean_train_df.columns.tolist(),
                                 lambda x: x not in ['waterfront', 'grade', 'condition', 'price'])].describe()
    stats.to_csv(Path('results', "Statistics.csv"))

    clean_train_df['waterfront'] = pd.Categorical(clean_train_df.waterfront)
    clean_train_df['grade'] = pd.Categorical(clean_train_df.grade)
    clean_train_df['condition'] = pd.Categorical(clean_train_df.condition)

    Xt = np.array(clean_train_df.drop("price", axis=1))
    Xv = np.array(clean_dev_df.drop("price", axis=1))


    ################ Main Algorithm ##########################################################
    # Adding 1 at the begining of data and weights to avoid separate bias vector
    trainingData = (np.c_[np.ones((len(clean_train_df), 1)), Xt],
                    np.array(clean_train_df["price"]).reshape(len(clean_train_df), 1))
    validationData = (np.c_[np.ones((len(clean_dev_df), 1)), Xv],
                      np.array(clean_dev_df["price"]).reshape(len(clean_dev_df), 1))

    # Main gradient descent
    theta = np.zeros((len(clean_train_df.columns), 1))
    training_output = gradient_descent(trainingData, validationData, theta,
                                    learning_rate=args.learning_rate, lmbda=args.lmbda, iterations=args.iterations)
    theta, cost_history, theta_history, gradient_history, validation_history, raw_theta_history = training_output


    ########## House Keeping Code ##########################################################
    print("##################")
    plotGradientDescent(cost_history, gradient_history, validation_history, theta, theta_history, "CGV",
                        args.learning_rate)

    # plotting each weight component
    for i in range(raw_theta_history[0].size):
        plt.plot(list(map(lambda i: i[11], raw_theta_history)))
        plt.savefig(Path('results', "plots", "RTH" + str(args.learning_rate) + "_" + str(i) + ".png"))
        plt.gcf().clear()

    # Append all evaluiation metrics to the main dump
    eval_path = Path('results','eval_dump.pk')
    evals = {} if not os.path.exists(eval_path) else  pk.load(open(eval_path, "rb"))
    evals[(args.learning_rate, args.lmbda)] = [theta, cost_history, theta_history, gradient_history, validation_history,
                                               raw_theta_history]
    pk.dump(evals, open(Path('results/eval_dump.pk'), "wb"))
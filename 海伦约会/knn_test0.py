import numpy as np
import operator
def classify(testset,dataset,labels,k):
    # numpy shape【0】返回数据集的行数
    datasetSize = dataset.shape[0]
    # print(datasetSize)
    #在列向量方向上重复inX共1次(横向)，行向量方向上重复inX共dataSetSize次(纵向)
    diffMat = np.tile(testset, (datasetSize, 1)) - dataset
    # print(diffMat)
    sqDiffMat = diffMat**2
    # print(sqDiffMat)
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    print(distances)
    sortedDistIndices = distances.argsort()
    print(sortedDistIndices)

    #定一个记录类别次数的字典
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndices[i]]
        #dict.get(key,default=None),字典的get()方法,返回指定键的值,如果值不在字典中返回默认值。
        #计算类别次数
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]


def createDataset():
    # 创建数据集
    group = np.array([[1,101],[5,89],[108,5],[115,8]])
    labels = ['爱情片','爱情片','动作片','动作片']
    return group,labels

if __name__ == '__main__':
    # 创建数据集
    group,labels=createDataset()
    testset = [50,50]

    test_class = classify(testset,group,labels,3)
    print(test_class)
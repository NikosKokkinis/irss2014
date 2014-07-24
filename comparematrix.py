import cPickle
import os, sys , numpy
import helpfunction

modellsi = "movielsi"
folderlsi= "lsi/"

def printInfo(recall,precision):
  recall = numpy.array(recall)
  precision = numpy.array(precision)
  print "General recall :"
  print recall
  print "General precision :"
  print precision
  print "Mean of recall :"
  print numpy.mean(recall)
  print "Mean of precision"
  print numpy.mean(precision)

def debugprint (gtm,sm,similarity,fileLength,recall,precision,fileNames,similarityMatrix,grundTrustMatrix,fileGMT):
  print " GTM row : "
  print grundTrustMatrix
  print "--"*30
  print "SM row: "
  print similarityMatrix
  print "--"*30
  print " GTM : "
  print gtm
  print "--"*30
  print "SM : "
  print sm
  print "--"*30
  print "Similarity : "
  print similarity
  print "--"*30
  print "Recall :"
  print recall
  print "--"*30
  print "Precision :"
  print precision
  print "--"*30
  print "fileTextLength :"
  print fileLength[os.path.basename(fileNames)]
  print "FileTextName :"
  print fileNames
  print "--"*30
  print "FileGTMName :"
  print fileGMT
  print "/"*30

def readFiles(foldername):
  fileNames = cPickle.load(open(folderName+folderlsi + modellsi + '.filenames', 'rb'))
  similarityMatrix = numpy.load(folderName + folderlsi+modellsi+'.npy')
  grundTrustMatrix = numpy.load(folderName + "gtm/AverageAnnotation.npy")
  filesGTM = numpy.load(folderName + "gtm/SceneNames.npy")
  return fileNames,similarityMatrix,filesGTM,grundTrustMatrix

def comparematrix(folderName,coefficient =1.2):
  fileNames,similarityMatrix,filesGTM,grundTrustMatrix = readFiles(folderName)
  recall = []
  precision = []
  recall2 = []
  precision2 = []
  for i in range(0,len(fileNames)):
    gtm=evaluateGTM(grundTrustMatrix[i],coefficient)
    sm=evaluateSM(similarityMatrix[i],coefficient)
    similarity = numpy.intersect1d(gtm,sm)
    recall_precision(gtm,sm,similarity,recall,precision)
    recall_precision_without_zeros(gtm,sm,similarity,recall2,precision2)
    #debugprint(gtm,sm,similarity,lenTextInFiles(folderName), recall[i],precision[i],fileNames[i],similarityMatrix[i],grundTrustMatrix[i],filesGTM[i])
  print "Compare Matrix (the most similar values)"
  printInfo (recall,precision)
  print "Compare Matrix (the most similar values without empty srt)"
  printInfo (recall2,precision2)


def recall_precision(gtm,sm,similarity,recall,precision):
  if len(gtm)!= 0 :
    recall.append(float(len(similarity))/float(len(gtm)))
  else :
    recall.append(0)
  if len(sm)!= 0 :
    precision.append(float(len(similarity))/float(len(sm)))
  else :
    precision.append(0)

def recall_precision_without_zeros(gtm,sm,similarity,recall,precision):
  if len(gtm)!= 0 and len(sm) !=0 and len(similarity) !=0 :
    recall.append(float(len(similarity))/float(len(gtm)))
    precision.append(float(len(similarity))/float(len(sm)))

def evaluateGTM(row, coef):
  T_value = 0
  index = numpy.transpose(numpy.nonzero(row))
  for val in range(0,len(index)):
    T_value += row[index[val]]
  if T_value <= 0 :
    T_value = 0
  else:
    T_value /= numpy.count_nonzero(row)
  result =[]
  indexOfResult=0
  for check in (row > T_value*coef):
    if check == True :
      result.append(indexOfResult)
    indexOfResult +=1
  return numpy.array(result)

def evaluateSM(row,coef):
  T_value = 0
  for val in range(0,len(row)):
    T_value += row[val]
  T_value /= len(row)-1
  result =[]
  indexOfResult=0
  for check in (row > T_value*coef):
    if check == True :
      result.append(indexOfResult)
    indexOfResult +=1
  return numpy.array(result)


def evaluateSMRandom(row,coef,length):
  random_index = numpy.random.permutation(len(row))
  #TODO: choose the number of return values
  T_value = 7 #length
  result =[]
  for i in range(0,int(T_value)):
    result.append(random_index[i])
  return numpy.array(result)


def evaluateMetric30per(row1, row2):
  indexofMatrix = row2.argsort()[-3:]
  #indexofMatrix = evaluateSMRandom(row2,1)*
  x=int(len(row1)/3)
  indexGTM = row1.argsort()[-x:]
  similarity = numpy.intersect1d(indexofMatrix,indexGTM)
  return (float(len(similarity))/3)

def comparematrix30percent(folderName,coefficient =1.2):
  fileNames,similarityMatrix,filesGTM,grundTrustMatrix = readFiles(folderName)
  result = []
  for i in range(0,len(fileNames)):
    result.append(evaluateMetric30per(grundTrustMatrix[i],similarityMatrix[i]))
  print "Compare matrixes in 30 % "
  print numpy.array(result)
  print "Mean of result"
  print numpy.mean(numpy.array(result))

def comparematrixRandom(folderName,coefficient =1.2):
  fileNames,similarityMatrix,filesGTM,grundTrustMatrix = readFiles(folderName)
  recall = []
  precision = []
  for i in range(0,len(fileNames)):
    gtm=evaluateGTM(grundTrustMatrix[i],coefficient)
    sm=evaluateSMRandom(similarityMatrix[i],coefficient,len(gtm))
    similarity = numpy.intersect1d(gtm,sm)
    recall_precision(gtm,sm,similarity,recall,precision)
    #debugprint(gtm,sm,similarity,helpfunction.lenTextInFiles(folderName), recall[i],precision[i],fileNames[i],similarityMatrix[i],grundTrustMatrix[i],filesGTM[i])
  print "Compare Matrix (random values from similarity text matrix)"
  printInfo (recall,precision)


if __name__ == '__main__':

  if sys.argv[1] == "-compare":
    folderName = sys.argv[2]
    comparematrix(folderName)
    comparematrixRandom(folderName)
    comparematrix30percent(folderName)
  if sys.argv[1] == "-compareMatrix":
    folderName = sys.argv[2]
    comparematrix(folderName)
  if sys.argv[1] == "-compareMatrixRandom":
    folderName = sys.argv[2]
    comparematrixRandom(folderName)
  if sys.argv[1] == "-compareMatrix30percent":
    folderName = sys.argv[2]
    comparematrix30percent(folderName)


  """
    #lenTextinFiles = lenTextInFiles(folderName)
    #newgrundTrustMatrix = transforMatrix(fileNames,filesGTM,grundTrustMatrix)
    if len(gtm)!= 0 and len(sm) !=0 and len(similarity) !=0 :
  """
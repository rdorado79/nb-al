import random
import math

def randomNormalizedVector(k):
  vec = [random.random() for x in range(k)]
  Z = sum(vec)
  return [x/Z for x in vec]


def p(point, mu, d):
  ret = 1
  for i in range(d):
    #if point[i] == 1:
    if point.has_key(i):
      ret*=mu[i]
    else:
      ret*=(1-mu[i]) 
  return ret


def logp(point, logmu, d):
  ret = 0
  for i in range(d):
    #if point[i] == 1:
    if point.has_key(i):
      ret+=logmu[i]
      #ret+=math.log(mu[i]+0.0000000001)
    else:
      ret+=math.log(1.0000000001-math.exp(logmu[i])) 
      #ret+=math.log(1.0000000001-mu[i]) 
  return ret


def sumlogexp(logs):
  maxlog = max(logs)
  acum = 0
  for x in logs:
    acum+=math.exp(x-maxlog)
  return maxlog + math.log(acum)


def clusterBeurnoulliMixtureSparseModel(k, points, d): 

  n = len(points)
  lambdas = randomNormalizedVector(k)
  loglambda = [math.log(x) for x in lambdas]
  #lambdas = [1/k for x in range(k)]
  mu = [[random.random() for x in range(d)] for x in range(k)]
  logmu = [[math.log(mu[j][i]) for i in range(d)] for j in range(k)]
  
  #print "\nInit lamdas: "
  #print lambdas
  #print "\nInit mus: "
  #print mu
  #print logmu
  #print "\n\n\n"

  it=0
  change=True

  oldloglikelihood=0
  while change:

    loglikelihood=0
    #loglikelihood2=0
    # Expectation
    Z = [[0.0 for x in range(k)] for x in range(n)]
    logZ = [[0.0 for x in range(k)] for x in range(n)]
    for i in range(n): 
      nsum=0
      for j in range(k):
        logZ[i][j]=loglambda[j] + logp(points[i], logmu[j], d)
        #loglikelihood2+=logZ[i][j]
        Z[i][j]=lambdas[j]*p(points[i], mu[j], d)
        loglikelihood+=math.log(Z[i][j]+0.0000000001)
        nsum+=Z[i][j]

        #print loglikelihood2
        #print str(loglikelihood)+"\n"
        #print "->"
        #print Z[i][j]
        #print math.exp(logZ[i][j])
        #print "->\n"

      #print logZ[i]
      sumlogZ = sumlogexp(logZ[i])
      #print str(i)+": "+str(nsum)
      #print str(i)+": "+str(math.exp(sumlogZ))+"\n"
      for j in range(k):
        Z[i][j]/=nsum
        logZ[i][j]-=sumlogZ
        #print str(math.exp(logZ[i][j]))
        #print str(Z[i][j])+"\n"
        
    if loglikelihood==oldloglikelihood:
      change=False
    else:
      oldloglikelihood=loglikelihood
    #  print math.exp(loglikelihood)

    # Maximization
    #sumZ = [[0.0 for x in range(d)] for x in range(k)]
    nlambdas = [0.0 for x in range(k)]
    nloglambda = [float('-inf') for x in range(k)]
    nmu = [[0.0 for x in range(d)] for x in range(k)]
    nlogmu = [[float('-inf') for x in range(d)] for x in range(k)]
    for i in range(k):
      skmu = 0
      sklogmu = 0
      for j in range(n):
        skmu+=Z[j][i]
        for m in range(d):
          if points[j].has_key(m):
            nmu[i][m]+=Z[j][i]
            nlogmu[i][m]=sumlogexp([nlogmu[i][m], logZ[j][i]])
        nlambdas[i] += Z[j][i] 
        nloglambda[i]=sumlogexp([nloglambda[i], logZ[j][i]])
      sklogmu = sumlogexp([logZ[j][i] for j in range(n)])
      #print str(skmu)+" "+str(math.exp(sklogmu))
      for m in range(d):
        #print "nmu  ("+str(i)+","+str(m)+") "+str(nmu[i][m])
        #print "nlmu ("+str(i)+","+str(m)+") "+str(math.exp(nlogmu[i][m]))+" \n"
        nmu[i][m]/=skmu 
        nlogmu[i][m]-=sklogmu
        #print "nmu  ("+str(i)+","+str(m)+") "+str(nmu[i][m])
        #print "nlmu ("+str(i)+","+str(m)+") "+str(math.exp(nlogmu[i][m]))+" \n"
      nlambdas[i]/=n
      nloglambda[i]-=math.log(n)
      #print "nlambda  ("+str(i)+") "+str(nlambdas[i])
      #print "nllambda ("+str(i)+") "+str(math.exp(nloglambda[i]))+"\n"
    #print nmu
    #print nlambdas
    mu = nmu
    logmu = nlogmu
    lambdas=nlambdas
    loglambda=nloglambda
    it+=1

    print "Iter "+str(it)+" finished...\n"
  ''' 
  # Calculate log-likelihood
  loglikelihood=0
  for i in range(n): 
    nsum=0
    for j in range(k):
      Z[i][j] = lambdas[j]*p(points[i], mu[j], d)  
  '''
  assignments = []
  maxpr = []
  for i in range(n):
    maxp=0
    assignments.append(0)
    maxpr.append(0)
    for j in range(k):
      #pr = lambdas[j]*p(points[i], mu[j], d)
      pr = logp(points[i], logmu[j], d)
      if maxp < pr: 
        maxp = pr
        assignments[i] = j
        maxpr[i] = pr

  print assignments
  print maxpr

  #print logmu
  #print loglambda




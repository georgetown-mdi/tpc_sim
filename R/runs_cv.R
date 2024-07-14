#!/usr/bin/Rscript
#  readruns.R Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 04.27.2024

library(FNN)
library(activegp)

tt <- Sys.time()

pnames <- names(jsonlite::read_json('pp_params.json'))

X <- as.matrix(read.csv("./random_X.csv"))
y <- read.csv("./random_y.csv")

# F1 score aka harmonic mean of two.
y <- 1/(1/y[,1]+1/y[,2])

## Compute projection.
groups <- sapply(strsplit(pnames, '_'), function(x) x[[1]])
gv <- unique(groups)
es <- list()
for (v in gv) {
    print(v)
    es[[length(es)+1]] <- as.numeric(groups==v)
}

P <- ncol(X)

Psimps <- lapply(es, function(e) e %*% t(e)/sum(e^2))
Pcps <- Reduce(function(x,y) x+y, Psimps, 0)
#eigen(Pcps, symmetric=T)[[1]]
proj <- diag(P)-Pcps
#eigen(proj, symmetric=T)[[1]]
##

## Subsamp
#subsize <- 300
subsize <- 20
reps <- 5
err_vanil <- rep(NA,reps)
err_proj <- rep(NA,reps)
for (rep in 1:reps) {
    test_inds <- sample(nrow(X),subsize)
    train_inds <- (1:nrow(X))[-test_inds]

    Xs <- X[train_inds,]
    ys <- y[train_inds]

    Lt <- Lt_GP(Xs, ys)
    Ztrain_vanil <- X[train_inds,] %*% Lt 
    Ztest_vanil <- X[test_inds,] %*% Lt 

    #Ztrain_proj <- X[train_inds,] %*% Lt %*% proj
    #Ztest_proj <- X[test_inds,] %*% Lt %*% proj
    Ztrain_proj <- X[train_inds,] %*% proj %*% Lt  
    Ztest_proj <- X[test_inds,] %*% proj %*% Lt 

    err_vanil[rep] <- sqrt(mean((FNN::knn.reg(train=Ztrain_vanil, test=Ztest_vanil, y=y[train_inds])$pred - y[test_inds])^2))
    err_proj[rep] <- sqrt(mean((FNN::knn.reg(train=Ztrain_proj, test=Ztest_proj, y=y[train_inds])$pred - y[test_inds])^2))
}

save(err_vanil, err_proj, file = 'runs_cv.RData')

print(Sys.time() - tt)

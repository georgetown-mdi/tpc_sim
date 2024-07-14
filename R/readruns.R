#!/usr/bin/Rscript
#  readruns.R Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 04.27.2024

library(activegp)

pnames <- names(jsonlite::read_json('pp_params.json'))

X <- as.matrix(read.csv("./random_X.csv"))
y <- read.csv("./random_y.csv")


# F1 score aka harmonic mean of two.
y <- 1/(1/y[,1]+1/y[,2])

Chat <- C_GP(X,y)

## Look at evals of raw matrix.
eigen(Chat)$values
v1 <- eigen(Chat)$vectors[,1]
names(v1) <- pnames
v2 <- eigen(Chat)$vectors[,2]
names(v2) <- pnames

Z = X %*% cbind(v1,v2) # Top direction is constant!

## Project along simplex constraint direction.
groups <- sapply(strsplit(pnames, '_'), function(x) x[[1]])
gv <- unique(groups)
es <- list()
for (v in gv) {
    print(v)
    es[[length(es)+1]] <- as.numeric(groups==v)
}

P <- dim(as.matrix(Chat))[1]

Psimps <- lapply(es, function(e) e %*% t(e)/sum(e^2))
Pcps <- Reduce(function(x,y) x+y, Psimps, 0)
#eigen(Pcps, symmetric=T)[[1]]
proj <- diag(P)-Pcps
#eigen(proj, symmetric=T)[[1]]

Chatproj <- proj %*% as.matrix(Chat) %*% proj

## Look at evals of raw matrix.
eigen(Chatproj)$values
v1 <- eigen(Chatproj)$vectors[,1]
names(v1) <- pnames
v2 <- eigen(Chatproj)$vectors[,2]
names(v2) <- pnames
v3 <- eigen(Chatproj)$vectors[,3]
names(v3) <- pnames

v1>1e-1
v2>1e-1
v3>1e-1

Z = X %*% cbind(v1,v2) # Top direction is constant!

plot_asm <- function(X, y, ed, main = '', xlab = '', ylab = '', fname = 'asm.pdf', useranks = TRUE) {
    Z <- X %*% ed$vectors[,1:2]

    fitZ <- hetGP::mleHomTP(Z, y)
    smooth_y <- predict(fitZ, Z)$mean

    fld <- akima::interp(x = Z[,1], y = Z[,2], z = smooth_y)

    pal = colorRampPalette(c("cadetblue1","red"))
    palpoint <- pal 
    KK <- 10
    if (useranks) {
        ycol <- rank(y)
    } else {
        print("Not using ranks!")
        ycol <- y
    }   
    cols <- palpoint(KK)[as.numeric(cut(ycol,breaks = KK))]

    # Plot results
    pdf(fname)
    par(mar=c(1.7,2.1,2,2)+0.1) #BLTR
    par(mgp=c(0.4,0.5,0))
    filled.contour(x = fld$x,
                   y = fld$y,
                   z = fld$z,
                   color.palette = pal,
                   main =main,
                   key.title = title(main = "Error", cex.main = 1), plot.axes = points(Z, bg = cols, pch = 21),
                   xlab = xlab,
                   ylab = ylab, 
                   cex.lab = 1.5, cex.main = 2)
    dev.off()
}

plot_asm(X, 1-y, eigen(Chatproj), xlab = 'ZIP Keyboard Error', ylab = 'First Name Insertions')

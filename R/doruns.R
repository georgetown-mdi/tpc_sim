#!/usr/bin/Rscript
#  doruns.R Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 04.25.2024

tt <- Sys.time()

Nh <- 350
reps <- 1
N <- reps*Nh
P <- 26

X <- matrix(NA,nrow=N,ncol=P)
y <-  matrix(NA,nrow=N,ncol=2)

for (n in 1:Nh) {
    ## Generate random setings.
    prms <- list()

    ## Corruptor params
    x <- runif(4)
    x <- x / sum(x)
    prms[['e1_ins']] <- x[1]
    prms[['e1_del']] <- x[2]
    prms[['e1_sub']] <- x[3]
    prms[['e1_trans']] <- x[4]

    x <- runif(4)
    x <- x / sum(x)
    prms[['e2_ins']] <- x[1]
    prms[['e2_del']] <- x[2]
    prms[['e2_sub']] <- x[3]
    prms[['e2_trans']] <- x[4]

    x <- runif(2)
    x <- x / sum(x)
    prms[['key_row']] <- x[1]
    prms[['key_col']] <- x[2]

    x <- runif(2)
    x <- x / sum(x)
    prms[['key_row']] <- x[1]
    prms[['key_col']] <- x[2]

    ## Corruptor combinations
    x <- runif(4)
    x <- x / sum(x)
    prms[['fn_e1']] <- x[1]
    prms[['fn_ocr']] <- x[2]
    prms[['fn_key']] <- x[3]
    prms[['fn_pho']] <- x[4]

    x <- runif(4)
    x <- x / sum(x)
    prms[['sn_sn']] <- x[1]
    prms[['sn_ocr']] <- x[2]
    prms[['sn_key']] <- x[3]
    prms[['sn_pho']] <- x[4]

    x <- runif(2)
    x <- x / sum(x)
    prms[['num_key']] <- x[1]
    prms[['num_pos']] <- x[2]

    x <- runif(2)
    x <- x / sum(x)
    prms[['date_e1']] <- x[1]
    prms[['date_e2']] <- x[2]

    x <- runif(2)
    x <- x / sum(x)
    prms[['date_e1']] <- x[1]
    prms[['date_e2']] <- x[2]

    x <- runif(4)
    x <- x / sum(x)
    prms[['city_e1']] <- x[1]
    prms[['city_miss']] <- x[2]
    prms[['city_key']] <- x[3]
    prms[['city_pho']] <- x[4]

    pjs <- jsonlite::toJSON(prms, auto_unbox = T, digits = NA)
    fileConn<-file("pp_params.json")
    writeLines(pjs, fileConn)
    close(fileConn)

    for (r in 1:reps) {
        ind <- (n-1)*reps + r
        ## Call parameterized_corruptor.R
        system2("./runmatch.sh")

        ## Read in results
        res <- read.table('param_f1.txt', sep='-')
        names(res) <- c("Precision","Recall")

        ## Store results
        X[ind,] <- as.numeric(prms)
        y[ind,] <- as.numeric(res)
    }
}

colnames(X) <- names(prms)
colnames(y) <- names(res)

print(Sys.time()-tt)

write.csv(X, "./random_X.csv", row.names = FALSE)
write.csv(y, "./random_y.csv", row.names = FALSE)

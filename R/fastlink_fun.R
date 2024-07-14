library(fastLink)
data(samplematch)

dfA
dfB

ret <- fastLink(dfA = dfA, dfB = dfB, varnames = c("firstname", "lastname", "city", "birthyear"))

ret$matches

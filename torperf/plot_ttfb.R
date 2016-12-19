### Copyright 2007 Steven J. Murdoch
### See LICENSE for licensing information

### XXX This script is broken, but we should look at it some more and
### maybe reuse parts of it when implementing Trac ticket #2563 (Add R
### code for processing Torperf data to the Torperf repository)

UFACTOR = 1e3
#library("gdata")
# install.packages("gdata", dependencies=c("Depends", "Imports"), repos = "http://cran.us.r-project.org")
library(gdata)
#install.packages("sROC", dependencies=c("Depends", "Imports"), repos = "http://cran.us.r-project.org")
#library(sROC)
# install.packages("EnvStats", dependencies=c("Depends", "Imports"), repos = "http://cran.us.r-project.org")
library(EnvStats)
#library(gtools)ca
# install.packages("RColorBrewer", dependencies=c("Depends", "Imports"), repos = "http://cran.us.r-project.org")
library(RColorBrewer)

# install.packages("Hmisc", dependencies=T, repos = "http://cran.us.r-project.org")
library("Hmisc")


varianz <- function(x) {n=length(x) ; var(x, na.rm = TRUE) * (n-1) / n}
stdabw <- function(x) {n=sum(!is.na(x)); sqrt(var(x, na.rm = TRUE) * (n-1) / n)}
std <- function(x) {sd(x, na.rm = TRUE)/sqrt(length(x))}


plotpercentile <- function(data, title, labels) {
medians <- data[[1]]
sds <- data[[2]]
# Create Line Chart

# print(medians[[1]])
# print(medians[[4]])
print(medians)
print(sds)

# print(length(data))
# print(length(data[1]))
# print(length(data[[1]]))
#
# print(length(medians))
# print(length(medians[1]))
# print(length(medians[[1]]))

n <- length(medians[[1]])
print(n)


#print(data)

# get the range for the x and y axis
minYrange <- 99999
maxYrange <- -9999
for (i in 1:4){
  tmp_min <- range(medians[[i]],finite=TRUE)[1]
  #print(tmp_min)
  if(tmp_min < minYrange && tmp_min > 0){
    minYrange <- tmp_min
    # cat("plotpercentile: Min:",i,minYrange,min(medians[[i]]),"\n")
  }
  if (range(medians[[i]],finite=TRUE)[2]>maxYrange){
    maxYrange <- range(medians[[i]],finite=TRUE)[2]
    #cat("plotpercentile: Max:",i,maxYrange,max(data[[i]]),"\n")
  }
}

xrange <- range(1:n)
#colors <- rainbow(6)
#colors<-gray.colors(6)
colors<-brewer.pal(4, "Dark2")
ltys <- c(2,1,2,2)

if (startsWith(title,"Percentile Throughput")){
yrange <- range(minYrange-5,maxYrange+5)
# set up the plot
plot(xrange, yrange, type="n", xlab="Dezile des Downloads in %",
     ylab="Durchsatz (KB/s)",yaxt="n",xaxt="n", cex.lab = 1.5)
axis(side=2, cex.axis=1.5)
# add a legend
#legend("bottomright", inset=.05, labels, col=unlist(colors), cex=0.7, horiz=FALSE, lty=unlist(ltys), lwd=3)
legend(xrange[1], yrange[2], labels, cex=2, col=colors, lty=ltys, lwd=3)
}
if (startsWith(title,"Percentile Latenz")){
yrange <- range(minYrange-0.05,maxYrange+0.05)
# set up the plot
plot(xrange, yrange, type="n", xlab="Dezile des Downloads in %",
     ylab="Latenz (sec)", yaxt="n",xaxt="n", cex.lab = 1.5)
axis(side=2, cex.axis=1.5)
# add a legend
legend("topright", inset=.05, labels, cex=2, col=colors, lty=ltys, lwd=3)
}
#print(xrange)
  # add lines
print("HUHU lines")

for (i in 1:4) {
  approach_median <- medians[[i]]
  approach_sd <- sds[[i]]
  a1 = NULL
  for(v in 1:9){a1 <- c(a1,approach_sd[[v]][1])}
  a2 = NULL
  for(v in 1:9){a2 <- c(a2,approach_sd[[v]][2])}
  # a1 <- approach_sd[[1]][1][1]
  lines(c(1:9), approach_median, type="b", lwd=3,
        lty=unlist(ltys)[i], col=colors[i], pch=19)
  Hmisc::errbar(c(1:9), approach_median, a1, a2, pch=2, add=T)
}

print("HUHU labs")
labs=c("10%","20%","30%","40%","50%","60%","70%","80%","90%")
axis(side=1, at=1:9, labels=labs, cex.axis=1.5)
grid(nx=NULL, ny=NULL)

# add a title and subtitle
#title(title)
}

plotpercentile_forTwo <- function(data, title, labels) {
medians <- data[[1]]
sds <- data[[2]]
# Create Line Chart
n <- length(medians[[1]])
#print(n)
#print(data)

# get the range for the x and y axis
minYrange <- 99999
maxYrange <- -9999
for (i in 1:2){
  tmp_min <- range(medians[[i]],finite=TRUE)[1]
  #print(tmp_min)
  if(tmp_min < minYrange && tmp_min > 0){
    minYrange <- tmp_min
    # cat("plotpercentile: Min:",i,minYrange,min(medians[[i]]),"\n")
  }
  if (range(medians[[i]],finite=TRUE)[2]>maxYrange){
    maxYrange <- range(medians[[i]],finite=TRUE)[2]
    #cat("plotpercentile: Max:",i,maxYrange,max(data[[i]]),"\n")
  }
}
# yrange <- range(minYrange,maxYrange)
xrange <- range(1:n)
#colors <- rainbow(6)
#colors<-gray.colors(6)
allcolors<-brewer.pal(4, "Dark2")
allltys <-  c(2,1,2,2)
ltys <- list()
colors <- list()
ApproachNames <- c("Vanilla1Guard", "Vanilla3Guards", "Gekürzt1Guard", "Gekürzt3Guards")
ApproachNames_Length <- c("","Vanilla","","Gekürzt")
ApproachNames_Guards <- c("1 Guard","3 Guards","","")


for (i in (1:length(ApproachNames))) {
  if (labels[1] == ApproachNames[i] | labels[1] == ApproachNames_Length[i] | labels[1] == ApproachNames_Guards[i]) {
    colors[1] <- allcolors[i]
    ltys[1] <- allltys[i]
    print(ltys)
    #print(colors)
  }
  if (length(labels)>1){
    if (labels[2] == ApproachNames[i] | labels[2] == ApproachNames_Length[i] | labels[2] == ApproachNames_Guards[i]) {
      colors[2] <- allcolors[i]
      ltys[2] <- allltys[i]
      #print(colors)
    }
  }
}


print("HUHU plot")
if (startsWith(title,"Percentile Throughput")){
yrange <- range(minYrange-5,maxYrange+7)
# set up the plot
plot(xrange, yrange, type="n", xlab="Dezile des Downloads in %",
     ylab="Durchsatz (KB/s)",yaxt="n",xaxt="n", cex.lab = 1.5)
axis(side=2, cex.axis=1.5)
# add a legend
#legend("bottomright", inset=.05, labels, col=unlist(colors), cex=0.7, horiz=FALSE, lty=unlist(ltys), lwd=3)
legend("bottomright",  inset=.05, labels, cex=2, col=unlist(colors), lty=unlist(ltys), lwd=3)
}
if (startsWith(title,"Percentile Latenz")){
yrange <- range(minYrange-0.03,maxYrange+0.04)
# set up the plot
plot(xrange, yrange, type="n", xlab="Dezile des Downloads in %",
     ylab="Latenz (sec)", yaxt="n",xaxt="n", cex.lab = 1.5)
axis(side=2, cex.axis=1.5)
# add a legend
legend("topright", inset=.05, labels, cex=2, col=unlist(colors), lty=unlist(ltys), lwd=3)

}
#print(xrange)
  # add lines
print("HUHU lines")

for (i in 1:2) {
  approach_median <- medians[[i]]
  approach_sd <- sds[[i]]
  a1 = NULL
  for(v in 1:9){a1 <- c(a1,approach_sd[[v]][1]); print(title); print(approach_sd[[v]][2]-approach_sd[[v]][1])}
  a2 = NULL
  for(v in 1:9){a2 <- c(a2,approach_sd[[v]][2])}
  # a1 = list()
  # for(v in 1:9){a1 <- c(a1,list(approach_sd[[v]][1])); print(title); print(approach_sd[[v]][2]-approach_sd[[v]][1])}
  # a2 = list()
  # for(v in 1:9){a2 <- c(a2,list(approach_sd[[v]][2]))}
  # print(title)
  # print()
  # print(range(a1,a2))
  # print(unlist(colors)[i])
  # print(unlist(ltys)[i])
  # print(a1)
  # print(approach_median)
  # print(typeof(unlist(a1)))
  # print(typeof(a2))
  # print(typeof(approach_median))
  Hmisc::errbar(c(1:9), approach_median, a1, a2, pch=2, col=unlist(colors)[i], add=T)
  # Hmisc::errbar(c(1:9), approach_median, c(2,4,30,4,5,9,1,9,1), c(1,10,100,52,1,6,8,90), pch=2, col=unlist(colors)[i], add=T)
  lines(c(1:9), approach_median, type="b", lwd=3,
        lty=unlist(ltys)[i], col=unlist(colors)[i], pch=19)
}
print("HUHU labs")
labs=c("10%","20%","30%","40%","50%","60%","70%","80%","90%")
axis(side=1, at=1:9, labels=labs, cex.axis=1.5)
# grid(nx=NULL, ny=NULL)

# add a title and subtitle
#title(title)
}

plotcdf_forTwo <- function(data, factor, labels, title, ylim=c(NA,NA)) {
## Scale units
#   if (factor == 1e6)
#     ylab <- "Time (s)"
if (factor == 1e3)
   xlab <- "Zeit (sec)"
else {
   xlab <- "Zeit (ms)"
   factor <- 1
}
if(title == "Throughput"){
  xlab <- "Durchsatz (kb/s)"
  d <- matrix()
  i<- 0
  for (approach in data){
    i <- i+1
    d[i]<-list(na.omit(approach)*factor)
  }
}else{
  #xlab <- ""
  d <- matrix()
  i<- 0
  for (approach in data){
    i <- i+1
    d[i]<-list(na.omit(approach)/factor)
  }
}


## Find plotting range
MinY<- NULL
MaxY <- NULL

#if it was a given parameter
if (!is.na(ylim[1]))
  MinY <- ylim[1]
if (!is.na(ylim[2]))
  MaxY <- ylim[2]

range <- 1.5

#if it was not given as a parameter
if(is.na(ylim[1])){
  for (i in (1:length(d))){
    for (col in d[i]) {
      s <- summary(col)
      Q1 <- as.vector(s[2])
      Q3 <- as.vector(s[5])
      InterQ <- Q3-Q1
      a <- Q1 - range*InterQ
      b <- Q3 + range*InterQ

      if (is.null(MinY) || a<MinY && a>0)
        MinY <- a
      #cat(MinY,MaxY,"\n")

      if (is.null(MaxY) || b>MaxY)
        MaxY <- b
      #cat(MinY,MaxY,"\n")
    }

  }
}

print(title)
## Find how many points this will cause to be skipped
skipped <- vector()
for (i in (1:length(d))) {
  col <- d[[i]]
  isSkipped <- col<MinY | col>MaxY
  #cat(MinY,MaxY,d[[i]][isSkipped],"\n")
  d[[i]][isSkipped] <- NA
  s <- length(which(isSkipped))
  ss <- paste("(",s,")",sep="")
  skipped <- append(skipped, ss)
  print(ss)
}





#allcolors<-rainbow(6)
allcolors<-brewer.pal(4, "Dark2")
allltys <-  c(2,1,2,2)
ltys <- list()
colors <- list()
ApproachNames <- c("Vanilla1Guard", "Vanilla3Guards", "Gekürzt1Guard", "Gekürzt3Guards")
ApproachNames_Length <- c("","Vanilla","","Gekürzt")
ApproachNames_Guards <- c("1 Guard","3 Guards","","")
for (i in (1:length(ApproachNames))) {
  if (labels[1] == ApproachNames[i] | labels[1] == ApproachNames_Length[i] | labels[1] == ApproachNames_Guards[i]) {
    colors[1] <- allcolors[i]
    ltys[1] <- allltys[i]
    print(ltys)
    #print(colors)
  }
  if (length(labels)>1){
    if (labels[2] == ApproachNames[i] | labels[2] == ApproachNames_Length[i] | labels[2] == ApproachNames_Guards[i]) {
      colors[2] <- allcolors[i]
      ltys[2] <- allltys[i]
      #print(colors)
    }
  }
}

colors<-c("red","black")

print(labels)
#labels <- mapply(paste, labels, skipped)
if (length(d)>1)
  title <- paste(title, " (", length(d[[1]]), " runs)", sep="")
else
  title <- paste(title, " (", length(d[[1]]), " runs, ", s, " skipped)", sep="")

#plot(ecdf(d[[1]]),lty=1,lwd=3,verticals=TRUE, col=unlist(colors)[1], do.points=FALSE, xlab=xlab,ylab="CDF",main=NULL)#main=title
ecdfPlot(d[[1]],ecdf.lty=unlist(ltys)[1],ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[1], xlab=xlab, ylab="CDF", cex.lab=1.5, cex.axis=1.5, main="", ylim=c(0.0,1.0))
if(length(d)>1){
  #lines(ecdf(d[[2]]),lty=5,lwd=3,verticals=TRUE, col=unlist(colors)[2], do.points=FALSE)
  ecdfPlot(d[[2]],ecdf.lty=unlist(ltys)[2],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[2], xlab=xlab, ylab="CDF", cex.lab=1.5, cex.axis=1.5, main="", ylim=c(0.0,1.0))
}
# axis(side=1, at=1:9, labels=labs, cex.axis=1.5)

cat("Quantil 1: ", quantile(d[[1]],0.5,na.rm = TRUE), "\n")
cat("Quantil 2: ", quantile(d[[2]],0.5,na.rm = TRUE), "\n")

# abline(h = 0.5,lty=3,lwd=1)
# abline(v = quantile(d[[1]],0.5,na.rm = TRUE),col=unlist(colors)[1],lty=3,lwd=1)
# if(length(d)>1){
#   abline(v = quantile(d[[2]],0.5,na.rm = TRUE),col=unlist(colors)[2],lty=3,lwd=1)
# }
# grid(nx=NULL, ny=NULL)
legend("bottomright", inset=.05, labels, col=unlist(colors), cex=2, horiz=FALSE, lty=unlist(ltys), lwd=3)

#   ## Plot the data
#   boxplot(names=labels, d, frame.plot=FALSE, ylab=ylab, range=range,
#           ylim=c(MinY, MaxY), xlab="Event (# points omitted)", main=title, notch=TRUE, cex.axis=0.9,
#           pars=list(show.names=TRUE, boxwex = 0.8, staplewex = 0.5, outwex = 0.5))
}

plotcdf <- function(data, factor, labels, ti, ylim=c(NA,NA)) {
## Scale units
#   if (factor == 1e6)
#     ylab <- "Time (s)"
if (factor == 1e3)
  xlab <- "Zeit (sec)"
else {
  xlab <- "Zeit (ms)"
  factor <- 1
}
if(ti == "Throughput"){
  xlab <- "Durchsatz (kb/s)"
  title <- "Durchsatz"
  d <- matrix()
  i<- 0
  for (approach in data){
    i <- i+1
    d[i]<-list(na.omit(approach)*factor)
  }
}else{
  #xlab <- ""
  title <- "Latenz"
  d <- matrix()
  i<- 0
  for (approach in data){
    i <- i+1
    d[i]<-list(na.omit(approach)/factor)
  }
}


## Find plotting range
MinY<- NULL
MaxY <- NULL

#if it was a given parameter
if (!is.na(ylim[1]))
  MinY <- ylim[1]
if (!is.na(ylim[2]))
  MaxY <- ylim[2]

range <- 1.5

#if it was not given as a parameter
if(is.na(ylim[1])){
  for (i in (1:length(d))){
    for (col in d[i]) {
      s <- summary(col)
      Q1 <- as.vector(s[2])
      Q3 <- as.vector(s[5])
      InterQ <- Q3-Q1
      a <- Q1 - range*InterQ
      b <- Q3 + range*InterQ

      if (is.null(MinY) || a<MinY && a>=0)
        MinY <- a
      #cat(MinY,MaxY,"\n")

      if (is.null(MaxY) || b>MaxY)
        MaxY <- b
      #cat(MinY,MaxY,"\n")
    }

  }
}

## Find how many points this will cause to be skipped
skipped <- vector()
for (i in (1:length(d))) {
  col <- d[[i]]
  isSkipped <- col<MinY | col>MaxY
  #cat(MinY,MaxY,d[[i]][isSkipped],"\n")
  d[[i]][isSkipped] <- NA
  s <- length(which(isSkipped))
  ss <- paste("(",s,")",sep="")
  skipped <- append(skipped, ss)
}

MinX<-NULL
MaxX<-NULL
for (i in (1:length(d))){
  tmp_min<- min(d[[i]], na.rm = TRUE)
  tmp_max<- max(d[[i]], na.rm = TRUE)
  if(is.null(MinX)){
    MinX<-tmp_min
  }
  else if(MinX>tmp_min){
    MinX<-tmp_min
  }
  if(is.null(MaxX)){
    MaxX<-tmp_max
  }
  else if(MaxX<tmp_max){
    MaxX<-tmp_max
  }
  }
  cat(MinX, MaxX, '\n')

#colors<-rainbow(6)
#colors<-gray.colors(6)
colors<-brewer.pal(4, "Dark2")
#allltys <- c(6,2,3,4,5,1)
#labels <- mapply(paste, labels, skipped)
if (length(d)>1)
  title <- paste(title, " (", length(d[[1]]), " runs)", sep="")
else
  title <- paste(title, " (", length(d[[1]]), " runs, ", s, " skipped)", sep="")

ltys <- c(2,1,2,2)

# plot(ecdf(d[[1]]), lty=1,lwd=3,verticals=TRUE, col=colors[1], do.points=FALSE, xlab=xlab,ylab="CDF",main=NULL)#,lty=unlist(ltys)[1])#,type="n")
# lines(ecdf(d[[2]]),lty=1,lwd=3,verticals=TRUE, col=colors[2], do.points=FALSE)#,lty=unlist(ltys)[2])#,type="n")
# lines(ecdf(d[[3]]),lty=1,lwd=3,verticals=TRUE, col=colors[3], do.points=FALSE)#,lty=unlist(ltys)[3])#,type="n")
# lines(ecdf(d[[4]]),lty=1,lwd=3,verticals=TRUE, col=colors[4], do.points=FALSE)#,lty=unlist(ltys)[4])#,type="n")
# lines(ecdf(d[[5]]),lty=1,lwd=3,verticals=TRUE, col=colors[5], do.points=FALSE)#,lty=unlist(ltys)[5])#,type="n")
# lines(ecdf(d[[6]]),lty=1,lwd=3,verticals=TRUE, col=colors[6], do.points=FALSE)#,lty=unlist(ltys)[6])#,type="n")
ecdfPlot(d[[1]],ecdf.lty=unlist(ltys)[1],ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[1], xlab=xlab, ylab="CDF",xlim=c(MinX, MaxX), main="")
ecdfPlot(d[[2]],ecdf.lty=unlist(ltys)[2],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[2], xlab=xlab, ylab="CDF", main="")
ecdfPlot(d[[3]],ecdf.lty=unlist(ltys)[3],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[3], xlab=xlab, ylab="CDF", main="")
ecdfPlot(d[[4]],ecdf.lty=unlist(ltys)[4],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[4], xlab=xlab, ylab="CDF", main="")
# ecdfPlot(d[[5]],ecdf.lty=unlist(ltys)[5],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[5], xlab=xlab, ylab="CDF", main="")
# ecdfPlot(d[[6]],ecdf.lty=unlist(ltys)[6],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[6], xlab=xlab, ylab="CDF", main="")
# ecdfPlot(d[[7]],ecdf.lty=unlist(ltys)[7],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[7], xlab=xlab, ylab="CDF", main="")
# ecdfPlot(d[[8]],ecdf.lty=unlist(ltys)[8],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[8], xlab=xlab, ylab="CDF", main="")



abline(h = 0.5,lty=3,lwd=1)
abline(v = quantile(d[[1]],0.5,na.rm = TRUE),col=colors[1],lty=3,lwd=1)
abline(v = quantile(d[[2]],0.5,na.rm = TRUE),col=colors[2],lty=3,lwd=1)
abline(v = quantile(d[[3]],0.5,na.rm = TRUE),col=colors[3],lty=3,lwd=1)
abline(v = quantile(d[[4]],0.5,na.rm = TRUE),col=colors[4],lty=3,lwd=1)
# abline(v = quantile(d[[5]],0.5,na.rm = TRUE),col=colors[5],lty=3,lwd=1)
# abline(v = quantile(d[[6]],0.5,na.rm = TRUE),col=colors[6],lty=3,lwd=1)
# abline(v = quantile(d[[7]],0.5,na.rm = TRUE),col=colors[7],lty=3,lwd=1)
# abline(v = quantile(d[[8]],0.5,na.rm = TRUE),col=colors[8],lty=3,lwd=1)

grid(nx=NULL, ny=NULL)
legend("bottomright", inset=.05, labels, col=colors, cex=1, horiz=FALSE, lty=ltys, lwd=3)

#   ## Plot the data
#   boxplot(names=labels, d, frame.plot=FALSE, ylab=ylab, range=range,
#           ylim=c(MinY, MaxY), xlab="Event (# points omitted)", main=title, notch=TRUE, cex.axis=0.9,
#           pars=list(show.names=TRUE, boxwex = 0.8, staplewex = 0.5, outwex = 0.5))
}

plotcdf_muliple_axis <- function(data, factor, labels, ti, ylim=c(NA,NA)) {
## Scale units

d <- matrix()
i <- 0
for (a in data){
  i <- i+1
  d[i]<-a
}

## Find plotting range
MinY_1<- NULL
MaxY_1 <- NULL
MinY_2 <- NULL
MaxY_2 <- NULL


#if it was a given parameter
if (!is.na(ylim[1]))
  MinY <- ylim[1]
if (!is.na(ylim[2]))
  MaxY <- ylim[2]

range <- 1.5

#if it was not given as a parameter
if(is.na(ylim[1])){
  for (i in (1:2)){
    for (col in d[i]) {
      s <- summary(col)
      Q1 <- as.vector(s[2])
      Q3 <- as.vector(s[5])
      InterQ <- Q3-Q1
      a <- Q1 - range*InterQ
      b <- Q3 + range*InterQ

      if (is.null(MinY_1) || a<MinY_1 && a>=0)
        MinY_1 <- a
      #cat(MinY,MaxY,"\n")

      if (is.null(MaxY_1) || b>MaxY_1)
        MaxY_1 <- b
      #cat(MinY,MaxY,"\n")
    }

  }
  for (i in (3:4)){
    for (col in d[i]) {
      s <- summary(col)
      Q1 <- as.vector(s[2])
      Q3 <- as.vector(s[5])
      InterQ <- Q3-Q1
      a <- Q1 - range*InterQ
      b <- Q3 + range*InterQ

      if (is.null(MinY_2) || a<MinY_2 && a>=0)
        MinY_2 <- a
      #cat(MinY,MaxY,"\n")

      if (is.null(MaxY_2) || b>MaxY_2)
        MaxY_2 <- b
      #cat(MinY,MaxY,"\n")
    }

  }
}

## Find how many points this will cause to be skipped
skipped <- vector()
for (i in (1:2)) {
  col <- d[[i]]
  isSkipped <- col<MinY_1 | col>MaxY_1
  #cat(MinY,MaxY,d[[i]][isSkipped],"\n")
  d[[i]][isSkipped] <- NA
  s <- length(which(isSkipped))
  ss <- paste("(",s,")",sep="")
  skipped <- append(skipped, ss)
}

skipped <- vector()
for (i in (3:4)) {
  col <- d[[i]]
  isSkipped <- col<MinY_2 | col>MaxY_2
  #cat(MinY,MaxY,d[[i]][isSkipped],"\n")
  d[[i]][isSkipped] <- NA
  s <- length(which(isSkipped))
  ss <- paste("(",s,")",sep="")
  skipped <- append(skipped, ss)
}

MinX_1<-NULL
MaxX_1<-NULL
for (i in 1:2){
  tmp_min<- min(d[[i]], na.rm = TRUE)
  tmp_max<- max(d[[i]], na.rm = TRUE)
  if(is.null(MinX_1)){
    MinX_1<-tmp_min
  }
  else if(MinX_1>tmp_min){
    MinX_1<-tmp_min
  }
  if(is.null(MaxX_1)){
    MaxX_1<-tmp_max
  }
  else if(MaxX_1<tmp_max){
    MaxX_1<-tmp_max
  }
  }
  cat(MinX_1, MaxX_1, '\n')

MinX_2<-NULL
MaxX_2<-NULL
for (i in 3:4){
  tmp_min<- min(d[[i]], na.rm = TRUE)
  tmp_max<- max(d[[i]], na.rm = TRUE)
  if(is.null(MinX_2)){
    MinX_2<-tmp_min
  }
  else if(MinX_2>tmp_min){
    MinX_2<-tmp_min
  }
  if(is.null(MaxX_2)){
    MaxX_2<-tmp_max
  }
  else if(MaxX_2<tmp_max){
    MaxX_2<-tmp_max
  }
  }
  cat(MinX_2, MaxX_2, '\n')

#colors<-rainbow(6)
#colors<-gray.colors(6)
# colors<-brewer.pal(4, "Dark2")
#allltys <- c(6,2,3,4,5,1)
#labels <- mapply(paste, labels, skipped)
title="Durchsatz und Latenz"
if (length(d)>1)
  title <- paste(title, " (", length(d[[1]]), " runs)", sep="")
else
  title <- paste(title, " (", length(d[[1]]), " runs, ", s, " skipped)", sep="")

ltys <- c(2,1,2,1)

# plot(ecdf(d[[1]]), lty=1,lwd=3,verticals=TRUE, col=colors[1], do.points=FALSE, xlab=xlab,ylab="CDF",main=NULL,xlim=c(MinX, MaxX))#,lty=unlist(ltys)[1])#,type="n")
# lines(ecdf(d[[2]]),lty=1,lwd=3,verticals=TRUE, col=colors[2], do.points=FALSE)#,lty=unlist(ltys)[2])#,type="n")
# par(new = TRUE)
# plot(ecdf(d[[3]]),lty=1,lwd=3,verticals=TRUE, col=colors[3], do.points=FALSE,axes=FALSE)#,lty=unlist(ltys)[3])#,type="n")
# lines(ecdf(d[[4]]),lty=1,lwd=3,verticals=TRUE, col=colors[4], do.points=FALSE)#,lty=unlist(ltys)[4])#,type="n")
# axis(side=3, at = pretty(range(d[[4]])))
# mtext("z", side=3, line=3)
# lines(ecdf(d[[5]]),lty=1,lwd=3,verticals=TRUE, col=colors[5], do.points=FALSE)#,lty=unlist(ltys)[5])#,type="n")
# lines(ecdf(d[[6]]),lty=1,lwd=3,verticals=TRUE, col=colors[6], do.points=FALSE)#,lty=unlist(ltys)[6])#,type="n")
# ecdfPlot(d[[1]],ecdf.lty=unlist(ltys)[1],ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[1], xlab=xlab, ylab="CDF", cex.lab=1.5, cex.axis=1.5, main="", yli/m=c(0.0,1.0))

ecdfPlot(d[[1]],ecdf.lty=unlist(ltys)[1],ecdf.lwd=3, curve.fill=FALSE,ecdf.col='black',xlab="", ylab="CDF", main="", cex.lab=1.5, cex.axis=1.5, ylim=c(0.0,1.0))
# par(new = TRUE)
ecdfPlot(d[[2]],ecdf.lty=unlist(ltys)[2],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col='black',axes=FALSE,ylim=c(0.0,1.0))
mtext("Latenz (sec):", side=1, line=1, at=-1.5, cex=1, col='black')

par(new = TRUE)
ecdfPlot(d[[3]],ecdf.lty=unlist(ltys)[3],add=FALSE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col='red',axes=FALSE,xlab="",ylab="",main="",ylim=c(0.0,1.0))#,xlim=c(MinX_2, MaxX_2)
# par(new = TRUE)
ecdfPlot(d[[4]],ecdf.lty=unlist(ltys)[4],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col='red', axes=FALSE, ylim=c(0.0,1.0))
axis(side=1, at = pretty(range(c(MinX_2, MaxX_2))), line=2, cex.lab=1.5, cex.axis=1.5, col.axis = 'red')
mtext("Durchsatz (kb/s):", side=1, line=2, at=-130, cex=1, col='red')
# ecdfPlot(d[[5]],ecdf.lty=unlist(ltys)[5],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[5], xlab=xlab, ylab="CDF", main="")
# ecdfPlot(d[[6]],ecdf.lty=unlist(ltys)[6],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[6], xlab=xlab, ylab="CDF", main="")
# ecdfPlot(d[[7]],ecdf.lty=unlist(ltys)[7],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[7], xlab=xlab, ylab="CDF", main="")
# ecdfPlot(d[[8]],ecdf.lty=unlist(ltys)[8],add=TRUE,ecdf.lwd=3, curve.fill=FALSE,ecdf.col=unlist(colors)[8], xlab=xlab, ylab="CDF", main="")


legend("bottomright", inset=.05, labels, col=c('black','black','red','red'), cex=1.5, horiz=FALSE, lty=ltys, lwd=3)

cat("Quantil 1: ", quantile(d[[1]],0.5,na.rm = TRUE), "\n")
cat("Quantil 2: ", quantile(d[[2]],0.5,na.rm = TRUE), "\n")

#   ## Plot the data
#   boxplot(names=labels, d, frame.plot=FALSE, ylab=ylab, range=range,
#           ylim=c(MinY, MaxY), xlab="Event (# points omitted)", main=title, notch=TRUE, cex.axis=0.9,
#           pars=list(show.names=TRUE, boxwex = 0.8, staplewex = 0.5, outwex = 0.5))
}

plotdist <- function(data, factor, labels, title, ylim=c(NA,NA)) {
## Scale units
#   if (factor == 1e6)
#     ylab <- "Time (s)"
if (factor == 1e3)
  ylab <- "Time (s)"
else {
  ylab <- "Time (ms)"
  factor <- 1
}
if(title == "Throughput"){
  ylab <- "Throughput in kb/s"

  d <- matrix()
  i<- 0
  for (approach in data){
    i <- i+1
    d[i]<-list(na.omit(approach)*factor)
  }
}else{

d <- matrix()
i<- 0
for (approach in data){
  i <- i+1
  d[i]<-list(na.omit(approach)/factor)
}
}

#    print(length(d))
#   print(length(d[[1]]))
#   print(length(d[[2]]))
#    print(length(d[[3]]))
#    print(length(d[[4]]))
#    print(length(d[[5]]))
#   print(length(d[[6]]))
# #   print(d[[1]])
# #   #print(data)
# #
##d <- na.omit(data)/factor

## Find plotting range
MinY<- NULL
MaxY <- NULL

#if it was a given parameter
if (!is.na(ylim[1]))
  MinY <- ylim[1]
if (!is.na(ylim[2]))
  MaxY <- ylim[2]

range <- 1.5

#if it was not given as a parameter
if(is.na(ylim[1])){
  for (i in (1:length(d))){
    for (col in d[i]) {
      s <- summary(col)
      Q1 <- as.vector(s[2])
      Q3 <- as.vector(s[5])
      InterQ <- Q3-Q1
      a <- Q1 - range*InterQ
      b <- Q3 + range*InterQ

      if (is.null(MinY) || a<MinY && a>=0)
        MinY <- a
        cat(MinY,MaxY,"\n")

      if (is.null(MaxY) || b>MaxY)
        MaxY <- b
        cat(MinY,MaxY,"\n")
    }

  }
}

## Find how many points this will cause to be skipped
skipped <- vector()
for (i in (1:length(d))) {
  col <- d[[i]]
  isSkipped <- col<MinY | col>MaxY
  #cat(MinY,MaxY,d[[i]][isSkipped],"\n")
  d[[i]][isSkipped] <- NA
  s <- length(which(isSkipped))
  ss <- paste("(",s,")",sep="")
  skipped <- append(skipped, ss)
}





labels <- mapply(paste, labels, skipped)
if (length(d)>1)
  title <- paste(title, " (", length(d[[1]]), " runs)", sep="")
else
  title <- paste(title, " (", length(d[[1]]), " runs, ", s, " skipped)", sep="")

## Plot the data
boxplot(names=labels, d, frame.plot=FALSE, ylab=ylab, range=range,
        ylim=c(MinY, MaxY), xlab="Approach (# points omitted)", main=title, notch=TRUE, cex.axis=0.7,
        pars=list(show.names=TRUE, boxwex = 0.8, staplewex = 0.5, outwex = 0.5))
}





removeOutliners <- function(filteredData){
removedFiltered <- filteredData
#print(filteredData)
for(i in 7:length(filteredData)-1){
    #print(quantile(filteredData[,i], probs=c(.25, .75), na.rm = TRUE))
    #print(IQR(filteredData[,i], na.rm = TRUE))
    qnt <- quantile(filteredData[,i], probs=c(.25, .75), na.rm = TRUE)
    H <- 1.5 * IQR(filteredData[,i], na.rm = TRUE)
    #removedFiltered[i] <- filteredData[i]
    #cat("Unten weg:",y[x < (qnt[1] - H)], "- oben weg:",y[x > (qnt[2] + H)],"\n")
    removedFiltered[filteredData[i] < (qnt[1] - H),i] <- NA
    #cat("Anzahl Removed unten:",length(which(is.na(y))),"\n")
    removedFiltered[filteredData[i] > (qnt[2] + H),i] <- NA
    #cat("Anzahl Removed beide:",length(which(is.na(y))),"\n")
  }
  return(removedFiltered)
}

substrRight <- function(x, n){
substr(x, nchar(x)-n+1, nchar(x))
}

plotMain <- function(ARGV) {

## process command line arguments
args <- unlist(strsplit(ARGV, " "))
if (length(args)<1) {
  dir <- ""
}
if (length(args)>1) {
  cat("Usage: R -f plot.R --args dir\n")
  stop("Wrong usage!")
}
if (length(args)==1) {
  if(args[1]=="." || args[1]=="./" || args[1]==""){
    dir <- ""
  } else if(substrRight(args[1],1)=="/"){
    dir <- args[1]
  }
  else if(substrRight(args[1],1)!="/"){
    dir <- paste(args[1],"/",sep="")
  }
}

print(dir)

## Read in filtered Data
short3Guard_HS1Guard_F <- sprintf("%s%s", dir,"short3Guard_HS1Guard_filtered.csv")
N_short3Guard_HS1Guard_S <- sprintf("cat %s | wc -l", short3Guard_HS1Guard_F)
N_short3Guard_HS1Guard <-as.numeric(system(N_short3Guard_HS1Guard_S,intern=TRUE))
short3Guard_HS1Guard <- read.csv(short3Guard_HS1Guard_F,nrows=N_short3Guard_HS1Guard-9)
#short3Guard_HS1Guard<-do.call(data.frame,lapply(short3Guard_HS1Guard, function(x) replace(x, is.infinite(x),NA)))
#is.na(short3Guard_HS1Guard) <- do.call(cbind,lapply(short3Guard_HS1Guard, is.infinite))

vanilla3Guard_HS1Guard_F <- sprintf("%s%s", dir,"vanilla3Guard_HS1Guard_filtered.csv")
N_vanilla3Guard_HS1Guard_S <- sprintf("cat %s | wc -l", vanilla3Guard_HS1Guard_F)
N_vanilla3Guard_HS1Guard <-as.numeric(system(N_vanilla3Guard_HS1Guard_S,intern=TRUE))
vanilla3Guard_HS1Guard <- read.csv(vanilla3Guard_HS1Guard_F)#,nrows=N_vanilla3Guard_HS1Guard-9)
#vanilla3Guard_HS1Guard <-do.call(data.frame,lapply(vanilla3Guard_HS1Guard, function(x) replace(x, is.infinite(x),NA)))
#is.na(vanilla3Guard_HS1Guard) <- do.call(cbind,lapply(vanilla3Guard_HS1Guard, is.infinite))

short3Guard_HS3Guard_F <- sprintf("%s%s", dir,"short3Guard_HS3Guard_filtered.csv")
N_short3Guard_HS3Guard_S <- sprintf("cat %s | wc -l", short3Guard_HS3Guard_F)
N_short3Guard_HS3Guard <-as.numeric(system(N_short3Guard_HS3Guard_S,intern=TRUE))
short3Guard_HS3Guard <- read.csv(short3Guard_HS3Guard_F)#,nrows=N_short3Guard_HS3Guard-9)
#short3Guard_HS3Guard <- do.call(data.frame,lapply(short3Guard_HS3Guard, function(x) replace(x, is.infinite(x),NA)))
#is.na(short3Guard_HS3Guard) <- do.call(cbind,lapply(short3Guard_HS3Guard, is.infinite))

vanilla3Guard_HS3Guard_F <- sprintf("%s%s", dir,"vanilla3Guard_HS3Guard_filtered.csv")
N_vanilla3Guard_HS3Guard_S <- sprintf("cat %s | wc -l", vanilla3Guard_HS3Guard_F)
N_vanilla3Guard_HS3Guard <-as.numeric(system(N_vanilla3Guard_HS3Guard_S,intern=TRUE))
vanilla3Guard_HS3Guard <- read.csv(vanilla3Guard_HS3Guard_F)#,nrows=N_vanilla3Guard_HS3Guard-9)
#vanilla3Guard_HS3Guard <- do.call(data.frame,lapply(vanilla3Guard_HS3Guard, function(x) replace(x, is.infinite(x),NA)))
#is.na(vanilla3Guard_HS3Guard) <- do.call(cbind,lapply(vanilla3Guard_HS3Guard, is.infinite))


pdf_filename <-  sprintf("%s%s", dir,"Plots_allApproaches.pdf")

pdf(file=pdf_filename,title = "Performance Plots of all Approaches")

ApproachNames <- c("vanilla3Guard_HS1Guard","vanilla3Guard_HS3Guard","short3Guard_HS1Guard","short3Guard_HS3Guard")

EventNames <- c("start",
              "socket()", "connect()", "auth", "SOCKS req", "SOCKS resp",
              "HTTP req", "HTTP resp", "HTTP done")


####WITHOUT OUTLIERS:
#Approaches <- c(short3Guard_HS1Guard,short3Guard_HS1Guard,vanilla3Guard_HS1Guard,vanilla3Guard_HS1Guard,short3Guard_HS3Guard,short3Guard_HS3Guard)
#Approaches_removed <- c(vanilla3Guard_HS1Guard_removed=NULL,short3Guard_HS1Guard_removed=NULL,vanilla3Guard_HS1Guard_removed=NULL,vanilla3Guard_HS1Guard_removed=NULL,short3Guard_HS3Guard_removed=NULL,short3Guard_HS3Guard_removed=NULL)
short3Guard_HS1Guard_removed <- removeOutliners(short3Guard_HS1Guard)
vanilla3Guard_HS1Guard_removed <- removeOutliners(vanilla3Guard_HS1Guard)
short3Guard_HS3Guard_removed <- removeOutliners(short3Guard_HS3Guard)
vanilla3Guard_HS3Guard_removed <-removeOutliners(vanilla3Guard_HS3Guard)
#print("HUHU Dezentile-Throughput-Median")

# ApproachNames <- c("vanilla3Guard_HS1Guard","vanilla3Guard_HS1Guard","vanilla1Guard_HS3Guard","vanilla3Guard_HS3Guard","short3Guard_HS1Guard","short3Guard_HS1Guard","short3Guard_HS3Guard","short3Guard_HS3Guard")

ApproachNames4 <- c("Vanilla1Guard", "Vanilla3Guards", "Gekürzt1Guard", "Gekürzt3Guards")

# pdf("Dezentile-Throughput-mean.pdf",title="Dezentile Throughput")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
#   c(mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE)),
#   c(mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE)),
#   c(mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE)),
#   c(mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE))
#   ),
# list(
#   c(list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int)),
#   c(list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int)),
#   c(list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int)),
#   c(list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int))
#   )
# )
# plotpercentile(data,"Percentile Throughput (mean)", ApproachNames4)
# dev.off()
#
# pdf("Dezentile-Latenz-mean.pdf",title="Dezentile Latenz")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
#   c(mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE)),
#   c(mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE)),
#   c(mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE)),
#   c(mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE))
#   ),
# list(
#   c(list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int)),
#   c(list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int)),
#   c(list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(short3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int)),
#   c(list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int))
#   )
# )
# plotpercentile(data,"Percentile Latenz (mean)", ApproachNames4)
# dev.off()
#
# print("Dezentile-Throughput-mean-VanillaShort")
#
# # ApproachNames4 <- c("Vanilla1Guards", "Vanilla3Guard", "Gekürzt1Guards", "Gekürzt3Guard")
# pdf("Dezentile-Throughput-mean-VanillaShort.pdf",title="Dezentile Throughput VanillaGekürzt")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
#   c(mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE)),
#   c(mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE))
#   ),
# list(
#   c(list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int)),
#   c(list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int))
#   )
# )
# plotpercentile_forTwo(data,"Percentile Throughput (mean)", c("Vanilla","Gekürzt"))
# dev.off()
#
# print("Dezentile-Latenz-mean-VanillaShort")
#
# pdf("Dezentile-Latenz-mean-VanillaShort.pdf",title="Dezentile Latenz VanillaGekürzt")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
#   c(mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE)),
#   c(mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE))
# ),
# list(
#   c(list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int)),
#   c(list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int))
#   )
# )
# plotpercentile_forTwo(data,"Percentile Latenz (mean)", c("Vanilla","Gekürzt"))#c(ApproachNames4[2], ApproachNames4[4]))
# dev.off()
# # ApproachNames4 <- c("Vanilla1Guard", "Vanilla3Guards", "Gekürzt1Guard", "Gekürzt3Guards")
#
# print("Dezentile-Throughput-mean-VanillaGuard")
#
# pdf("Dezentile-Throughput-mean-VanillaGuard.pdf",title="Dezentile Throughput Vanilla Guard")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
# c(mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE)),
# c(mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE))
# ),
# list(
# c(list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int)),
# c(list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int))
#   )
# )
# plotpercentile_forTwo(data,"Percentile Throughput (mean)", c("1 Guard", "3 Guards"))#c(ApproachNames4[1], ApproachNames4[2]))
# dev.off()
#
# pdf("Dezentile-Latenz-mean-VanillaGuard.pdf",title="Dezentile Latenz VanillaGuard")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
#   c(mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE)),
#   c(mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE))
#   ),
# list(
#   c(list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int)),
#   c(list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int))
#   )
# )
# plotpercentile_forTwo(data,"Percentile Latenz (mean)", c("1 Guard", "3 Guards"))
# dev.off()
#
# pdf("Dezentile-Throughput-mean-ShortGuard.pdf",title="Dezentile Throughput Gekürzt Guard")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
# c(mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE)),
# c(mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000,na.rm=TRUE))
# ),
# list(
# c(list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int)),
# c(list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC1_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC2_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC3_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC4_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC5_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC6_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC7_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC8_KBms*1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$TROUGHPUT_PERC9_KBms*1000)$conf.int))
# )
# )
# plotpercentile_forTwo(data,"Percentile Throughput (mean)", c(ApproachNames4[3], ApproachNames4[4]))
# dev.off()
#
# pdf("Dezentile-Latenz-mean-ShortGuard.pdf",title="Dezentile Latenz GekürztGuard")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data <- list(
# list(
# c(mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE)),
# c(mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000,na.rm=TRUE),mean(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000,na.rm=TRUE))
# ),
# list(
# c(list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(vanilla3Guard_HS1Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int)),
# c(list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME1_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME2_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME3_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME4_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME5_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME6_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME7_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME8_MS/1000)$conf.int),list(t.test(short3Guard_HS3Guard_removed$LAT_DATAPERCTIME9_MS/1000)$conf.int))
# )
# )
# plotpercentile_forTwo(data,"Percentile Latenz (mean)", c(ApproachNames4[3], ApproachNames4[4]))
# dev.off()
#
# ApproachNames4 <- c("Vanilla1Guard", "Vanilla3Guards", "Gekürzt1Guard", "Gekürzt3Guards")
#
# pdf("Latenz-CDF.pdf",title="Latenz")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(vanilla3Guard_HS1Guard$LATENZ_MS,vanilla3Guard_HS3Guard$LATENZ_MS,short3Guard_HS1Guard$LATENZ_MS,short3Guard_HS3Guard$LATENZ_MS)
# plotcdf(data, 1e3, ApproachNames4, "Latenz") #c(0,12)
# dev.off()
#
#
# pdf("Throughput-CDF.pdf",title="Throughput")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(vanilla3Guard_HS1Guard$TROUGHPUT_KBms,vanilla3Guard_HS3Guard$TROUGHPUT_KBms,short3Guard_HS1Guard$TROUGHPUT_KBms,short3Guard_HS3Guard$TROUGHPUT_KBms)
# plotcdf(data, 1e3, ApproachNames4, "Throughput")#c(0,800)
# dev.off()
#
pdf("Throughput-VanillaShort.pdf", title="Throughput Vanilla vs Short CDF")
par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
data<-list(vanilla3Guard_HS3Guard$TROUGHPUT_KBms, short3Guard_HS3Guard$TROUGHPUT_KBms)
plotcdf_forTwo(data, 1e3,c("Vanilla", "Gekürzt"),"Throughput") #,c(0,12))
dev.off()
#
# pdf("Latenz-VanillaShort.pdf",title="Latenz  Vanilla vs Short CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(vanilla3Guard_HS3Guard$LATENZ_MS, short3Guard_HS3Guard$LATENZ_MS)
# plotcdf_forTwo(data, 1e3,c("Vanilla", "Gekürzt"),"Latenz")
# dev.off()
#
# pdf("Throughput-VanillaGuards.pdf", title="Throughput Vanilla CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(vanilla3Guard_HS3Guard$TROUGHPUT_KBms, vanilla3Guard_HS1Guard$TROUGHPUT_KBms)
# plotcdf_forTwo(data, 1e3,c("3 Guards", "1 Guard"),"Throughput")
# dev.off()
#
# pdf("Latenz-VanillaGuards.pdf",title="Latenz  Vanilla CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(vanilla3Guard_HS3Guard$LATENZ_MS, vanilla3Guard_HS1Guard$LATENZ_MS)
# plotcdf_forTwo(data, 1e3,c("3 Guards", "1 Guard"),"Latenz")
# dev.off()
#
# pdf("Throughput-ShortGuards.pdf", title="Throughput Short CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(short3Guard_HS3Guard$TROUGHPUT_KBms, short3Guard_HS1Guard$TROUGHPUT_KBms)
# plotcdf_forTwo(data, 1e3,c("Gekürzt3Guards", "Gekürzt1Guard"),"Throughput")
# dev.off()
#
# pdf("Latenz-ShortGuards.pdf",title="Latenz  Short CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(short3Guard_HS3Guard$LATENZ_MS, short3Guard_HS1Guard$LATENZ_MS)
# plotcdf_forTwo(data, 1e3,c("Gekürzt3Guards", "Gekürzt1Guard"),"Latenz")
# dev.off()

ttfb_vanilla <- (vanilla3Guard_HS3Guard$DATARESPONSE_MS-vanilla3Guard_HS3Guard$DATARREQUEST_MS)
ttfb_short <- (short3Guard_HS3Guard$DATARESPONSE_MS-short3Guard_HS3Guard$DATARREQUEST_MS)

# pdf("Latenz-TTFB-CDF.pdf",title="Latenz TTFB")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(vanilla3Guard_HS1Guard$DATARESPONSE_MS,vanilla3Guard_HS3Guard$DATARESPONSE_MS,short3Guard_HS1Guard$DATARESPONSE_MS,short3Guard_HS3Guard$DATARESPONSE_MS)
# plotcdf(data, 1e3, ApproachNames4, "Latenz TTFB") #c(0,12)
# dev.off()

pdf("Latenz-TTFB-VanillaShort.pdf",title="Latenz TTFB Vanilla vs Short CDF")
par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
data<-list(vanilla3Guard_HS3Guard$DATARESPONSE_MS, short3Guard_HS3Guard$DATARESPONSE_MS)
plotcdf_forTwo(data, 1e3,c("Vanilla", "Gekürzt"),"Latenz")
dev.off()

# pdf("Latenz-TTFB-VanillaGuards.pdf",title="Latenz TTFB Vanilla CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list(vanilla3Guard_HS3Guard$DATARESPONSE_MS, vanilla3Guard_HS1Guard$DATARESPONSE_MS)
# plotcdf_forTwo(data, 1e3,c("3 Guards", "1 Guard"),"Latenz")
# dev.off()

# print("Latenz Dataresponse-Datarequest VanillaShort CDF")
# pdf("Latenz-Dataresponse-Datarequest-VanillaShort.pdf",title="Latenz Dataresponse-Datarequest VanillaShort CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list((vanilla3Guard_HS3Guard$DATARESPONSE_MS - vanilla3Guard_HS3Guard$DATARREQUEST_MS), (short3Guard_HS3Guard$DATARESPONSE_MS - short3Guard_HS3Guard$DATARREQUEST_MS))
# plotcdf_forTwo(data, 1e3,c("Vanilla", "Gekürzt"),"Latenz")
# dev.off()

# print("Latenz Dataresponse-Response VanillaShort CDF")
# pdf("Latenz-Dataresponse-Response-VanillaShort.pdf",title="Latenz Dataresponse-Response VanillaShort CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list((vanilla3Guard_HS3Guard$DATARESPONSE_MS - vanilla3Guard_HS3Guard$RESPONSE_MS), (short3Guard_HS3Guard$DATARESPONSE_MS - short3Guard_HS3Guard$RESPONSE_MS))
# plotcdf_forTwo(data, 1e3,c("Vanilla", "Gekürzt"),"Latenz")
# dev.off()


# print("Latenz Dataresponse-Request VanillaShort CDF")
# pdf("Latenz-Dataresponse-Request-VanillaShort.pdf",title="Latenz Dataresponse-Request VanillaShort CDF")
# par(mar=c(3.5,3.8,0.1,0.1)+0.1,mgp=c(2.6,1,0))
# data<-list((vanilla3Guard_HS3Guard$DATARESPONSE_MS - vanilla3Guard_HS3Guard$REQUEST_MS), (short3Guard_HS3Guard$DATARESPONSE_MS - short3Guard_HS3Guard$REQUEST_MS))
# plotcdf_forTwo(data, 1e3,c("Vanilla", "Gekürzt"),"Latenz")
# dev.off()

# pdf("TTFB-Durchsatz-VanillaShort.pdf",title="TTFB Durchsatz Vanilla vs Short CDF")
# par(mar=c(4,6,0.1,0.1) + 0.3,mgp=c(2.6,1,0))
# data<-list(list(na.omit(vanilla3Guard_HS3Guard$DATARESPONSE_MS)/1e3),
#   list(na.omit(short3Guard_HS3Guard$DATARESPONSE_MS)/1e3),
#   list(na.omit(vanilla3Guard_HS3Guard$TROUGHPUT_KBms)*1e3),
#   list(na.omit(short3Guard_HS3Guard$TROUGHPUT_KBms)*1e3))
# plotcdf_muliple_axis(data, 1e3,c("Latenz_Vanilla", "Latenz_Gekürzt", "Durchsatz_Vanilla", "Durchsatz_Gekürzt"),"Latenz&Durchsatz")
# dev.off()

# pdf("Latenz-Durchsatz-VanillaShort.pdf",title="Latenz Durchsatz Vanilla vs Short CDF")
# par(mar=c(3.5,3.8,4,0.1) + 0.3,mgp=c(2.6,1,0))
# data<-list(list(na.omit(vanilla3Guard_HS3Guard$LATENZ_MS)/1e3),
#   list(na.omit(short3Guard_HS3Guard$LATENZ_MS)/1e3),
#   list(na.omit(vanilla3Guard_HS3Guard$TROUGHPUT_KBms)*1e3),
#   list(na.omit(short3Guard_HS3Guard$TROUGHPUT_KBms)*1e3))
# plotcdf_muliple_axis(data, 1e3,c("Latenz_Vanilla", "Latenz_Gekürzt", "Durchsatz_Vanilla", "Durchsatz_Gekürzt"),"Latenz&Durchsatz")
# dev.off()

########################################################################################
# Data Export
########################################################################################
d<-vanilla3Guard_HS3Guard$TROUGHPUT_KBms*1e3
f = ecdf(d)
write.table(cbind(sort(d), f(sort(d))), file="throughput-vanilla.dat", col.names = F, row.names = F, sep=" ")

d<-short3Guard_HS3Guard$TROUGHPUT_KBms*1e3
f = ecdf(d)
write.table(cbind(sort(d), f(sort(d))), file="throughput-short.dat", col.names = F, row.names = F, sep=" ")
# paste throughput-short.dat throughput-vanilla.dat > throughput.dat

d<-vanilla3Guard_HS3Guard$DATARESPONSE_MS/1e3
f = ecdf(d)
write.table(cbind(sort(d), f(sort(d))), file="ttfb-vanilla.dat", col.names = F, row.names = F, sep=" ")

d<-short3Guard_HS3Guard$DATARESPONSE_MS/1e3
f = ecdf(d)
write.table(cbind(sort(d), f(sort(d))), file="ttfb-short.dat", col.names = F, row.names = F, sep=" ")
# paste ttfb-short.dat ttfb-vanilla.dat > ttfb.dat
########################################################################################

}

plotMain(commandArgs(TRUE))
warnings()

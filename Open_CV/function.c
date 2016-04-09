// http://www.cnblogs.com/mengdd/archive/2012/08/01/2619043.html
// http://www.faceplusplus.com.cn/demo-search/  ??–Ê•”ã¤â‹


CvSeq* cvHaarDetectObjects( 
const CvArr* image, 
CvHaarClassifierCascade* cascade, 
CvMemStorage* storage, 
double scale_factor CV_DEFAULT(1.1), 
int min_neighbors CV_DEFAULT(3), 
int flags CV_DEFAULT(0), 
CvSize min_size CV_DEFAULT(cvSize(0,0)), 
CvSize max_size CV_DEFAULT(cvSize(0,0)) 
);
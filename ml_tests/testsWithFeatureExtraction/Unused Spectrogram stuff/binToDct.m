function [c] = binToDct(fnameIn, fnameout, fnameBin)
%spec code
datToImage_77(fnameIn, fnameout, fnameBin);

%DCT code
I = imread(fnameout);
%delete fnameout
I = rgb2gray(I);
I = im2double(I);

T = dct(I);

c = T(1:500);

end
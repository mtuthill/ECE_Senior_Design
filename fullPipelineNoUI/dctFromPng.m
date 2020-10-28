function [c] = dctFromPng(fname)
%DCT code
I = imread(fname);
I = rgb2gray(I);
I = im2double(I);

T = dct(I);

c = T(1:500);

end
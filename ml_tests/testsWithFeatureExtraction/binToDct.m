function [c] = binToDct(fname, fout)
%spec code
microDoppler_AWR1642_bulk_BPM(fname, fout);

%DCT code
I = imread(".png");
delete .png
I = rgb2gray(I);
I = im2double(I);

T = dct(I);

c = T(1:500);

end
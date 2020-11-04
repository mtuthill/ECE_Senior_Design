function [ ] = datToImageV1_custom( fNameIn, fNameOut, fNameOut2, fnameBin)
    fileID = fopen(fNameIn, 'r'); % open file
    Data = fread(fileID, 'int16');% DCA1000 should read in two's complement data
    %zero extend
    A = zeros(39321600, 1);
    Data(end+1:numel(A))=0;
    fclose(fileID); % close file

    numADCBits = 16; % number of ADC bits per sample
    numLanes = 4; 
    fstart = 77.1799e9; % Start Frequency
    fstop = 77.9474e9; % Stop Frequency
    fc = (fstart+fstop)/2; % Center Frequency
    c = physconst('LightSpeed'); % Speed of light
    lambda = c/fc; % Lambda
    SweepTime = 40e-3; % Time for 1 frame=sweep
    NTS = 256; % Number of time samples per sweep                               
    NPpF = 128; % Number of pulses per frame
    NoF = 150; % Number of frames
    Bw = fstop - fstart; % Bandwidth
    sampleRate = 10e6; % Smpling Rate
    dT = SweepTime/NPpF; % 
    prf = 1/dT; 
    timeAxis = [1:NPpF*NoF]*SweepTime/NPpF ; % Time
    duration = max(timeAxis);
    freqAxis = linspace(-prf/2,prf/2-prf/4096,4096); % Frequency Axis
    
    % reshape and combine real and imaginary parts of complex number
    Data = reshape(Data, numLanes*2, []);
    Data = Data(1:4,:) + sqrt(-1)*Data(5:8,:);                                  
    Data = Data.';
    Np = floor(size(Data(:,1),1)/NTS); % #of pulses
    
    clearvars fileID dataArray ans;
%% IQ Correction                                                          
% rawData = zeros(NTS,Np,numLanes);
% fftRawData = zeros(NTS,Np,numLanes);
% for ii = 1:4
%     I_rawData(:,ii) = real(Data(:,ii)); % Real Data
%     Q_rawData(:,ii) = imag(Data(:,ii)); % Imaginary Data
%     Data_Complex(:,ii) = IQcorrection(I_rawData(:,ii),Q_rawData(:,ii)); % Complex Data
%     Colmn = floor(length(Data_Complex(:,1))/NTS);
%     rawData(:,:,ii) = reshape(Data_Complex(:,ii),NTS,Colmn);
%     fftRawData(:,:,ii) = fftshift(fft(rawData(:,:,ii)),1);
%     rp((1:NTS/2),:,ii) = fftRawData(((NTS/2+1):NTS),:,ii); %range profile,color space
% end
%% No IQ Correction
rawData = zeros(NTS,Np,numLanes);
fftRawData = zeros(NTS,Np,numLanes);
for ii = 1:4
    Colmn = floor(length(Data(:,1))/NTS);
    rawData(:,:,ii) = reshape(Data(:,ii),NTS,Colmn);
    fftRawData(:,:,ii) = fftshift(fft(rawData(:,:,ii)),1);
    rp((1:NTS/2),:,ii) = fftRawData(((NTS/2+1):NTS),:,ii); %range profile,color space
end
%% MTI Filter
    [m,n]=size(rp(:,:,1));
    ns = size(rp,2)+4;                                                      % why +4
    h=[1 -2 3 -2 1]';                                                      % where h indxs come from
    rngpro=zeros(m,ns);
    for k=1:m
        rngpro(k,:)=conv(h,rp(k,:,1));
    end
%% Micro-DopplerSpectrogram Data  Time vs Freq

    rng_axis = ([1:NTS]-1)*c/2/Bw;
    nfft = 2^12;window = 256;noverlap = 197;shift = window - noverlap; 
    
    sx = myspecgramnew(sum(rngpro(1:15,:),1),window,nfft,shift);                  % why row 8?
    sx1 = fftshift(sx,1);
    time = dT * length(Data)/NTS;
    %save(fNameOut2, 'sx1'); % save complex spect matrix
    fig = figure('units','normalized','outerposition',[0 0 1 1]); % [left bottom width height]
    colormap(jet(256));
    doppSignMTI = imagesc(timeAxis,[-prf/2 prf/2],20*log10(abs(sx1/max(max(abs(sx1))))));
    axis off
    caxis([-45 0])
    axis([0 20 -500 500])
    F = getframe(gca);
    [X, ~] = frame2im(F);
    fnamepng = strcat(fnameBin(1:end-4),'.png');
    fnamegray = strcat(fnameBin(1:end-4),'_gray.png');
    fnamefig = strcat(fNameOut, '\', fnameBin(1:end-4),'.fig');
    imwrite(X,fNameOut);
    %saveas(fig,fnamefig);
    colormap(gray);
    F = getframe(gca);
    [X2, ~] = frame2im(F);
    %imwrite(X2,fullfile(fNameOut, fnamegray));
    clear Data
    close all
end
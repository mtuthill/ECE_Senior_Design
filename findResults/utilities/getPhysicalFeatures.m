function f = getPhysicalFeatures(img_matrix)

total_pow = sum(img_matrix);
upper_lim = 0.97*total_pow;
central_lim = 0.5*total_pow;
lower_lim = 0.03*total_pow;

upper_env = zeros(1,size(img_matrix,2));
central_env = zeros(1,size(img_matrix,2));
lower_env = zeros(1,size(img_matrix,2));

Sum = 0;
%% Upper Envelope
for t = 1:size(img_matrix,2)  
    for v = size(img_matrix,1):-1:1
        Sum = Sum + img_matrix(v,t);
        if Sum > upper_lim(t)
            Sum = 0;
            break
        end
    end
    upper_env(t) = v;
end
%% Lower envelope
for t = 1:size(img_matrix,2)  
    for v = size(img_matrix,1):-1:1
        Sum = Sum + img_matrix(v,t);
        if Sum > lower_lim(t)
            Sum = 0;
            break
        end
    end
    lower_env(t) = v;
end
%% Central envelope
for t = 1:size(img_matrix,2)  
    for v = size(img_matrix,1):-1:1
        Sum = Sum + img_matrix(v,t);
        if Sum > central_lim(t)
            Sum = 0;
            break
        end
    end
    central_env(t) = v;
end

[upperEnvPeaks] = findpeaks(upper_env);

invertedY = max(lower_env) - lower_env;
[lowerEnvPeaks] = findpeaks(invertedY);

f(1) = mean(upperEnvPeaks) - mean(lowerEnvPeaks); % bandwidth

f(2) = mean(horzcat(upperEnvPeaks, lowerEnvPeaks)); %offset

invertedY = max(upper_env) - upper_env;
[upperEnvValleys] = findpeaks(invertedY);

[lowerEnvValleys] = findpeaks(lower_env);

f(3) = mean(upperEnvValleys) - mean(lowerEnvValleys); % BW w/o uD

f(4) = std(img_matrix) / mean(img_matrix); %normalized std of signal strength

end
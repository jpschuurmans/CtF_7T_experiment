%% alpha blending the stimuli in the white noise
% one way (as close as what xpman program does):
% a weighted sum of the luminance values of each pixel of the image
% and the background. 

close all; clear; clc

basefolder = 'C:/Users/Adminuser/Documents/04_CtF-7T/Experiment/stimuli_matlab/';
outfolder_stim = [basefolder 'finalstim/stimuli/'];
outfolder_back = [basefolder 'finalstim/background/'];
outfolder_mask = [basefolder 'finalstim/masks/'];
load([basefolder 'RPV1_STIM.mat'])
addpath(basefolder)

backgrounds = length(imset.iter_back);

outputmat = 'RPV1_BLEND.mat';

%%%%%%%%%%%% load this blurry mask
%%%%%%%%%%%% make sure the face is just as big as the stimuli
[MaskIm,~,MaskAlpha] = (imread([basefolder 'blurrymask.png']));
%imshow(MaskAlpha)
MaskAlpha = single(MaskAlpha); MaskAlpha = imresize(MaskAlpha,(1/scalefactor(1)));
cut = round((length(MaskAlpha)-desired_size(1))/2);
MaskAlpha = MaskAlpha./max(MaskAlpha(:));
MaskAlpha = MaskAlpha(cut:end-(cut+1),cut:end-(cut+1));

imwrite(MaskAlpha,[outfolder_mask 'alphamask.bmp'],'BMP')

ellipseBack = find(MaskAlpha == MaskAlpha(1));
ellipseCenter = find(MaskAlpha < MaskAlpha(1));

%LC = [0.45 0.1]; % desired luminance and contrast
%maskcontrast = 0.15; % mask had higher contrast for masking efficiency

stimuli = {'mask' '60' '35' '0'}; %stimuli and mask
stimuli = {'15' '25' '70' '80'}; %stimuli and mask
stimuli = {'30' '55'}

%preallocate for speed
finalstim_backpixLC = cell(backgrounds,length(stimuli)); %preallocate
finalstim_facepixLC = cell(backgrounds,length(stimuli)); %preallocate
finalbackim_backpixLC = cell(backgrounds,length(stimuli)); %preallocate
finalbackim_facepixLC = cell(backgrounds,length(stimuli)); %preallocate

for theback = 1:backgrounds % for all scrambled backgrounds
    fprintf('bleding and saving images for %d background \n',theback)
    backname = ['BG' num2str(theback)];

    for thestim = 1:length(stimuli) %stim, maskLSF, maskHSF
        %naming for checking and saving
        stimulus  = char(stimuli(thestim));
        if strcmp(stimulus,'mask')
            set = imset.mask;
            signal = 1; % noise = 1-signal
            face_LC = [LC(1) maskcontrast]; % desired luminance and contrast
        else
            set = imset.eq_stim;
            signal = str2double(stimulus)/100;
            face_LC = LC; % desired luminance and contrast
        end
        noise = 1-signal; % for the background
        
        for theface = 1:length(nim) %for all faces
            % this first part is for blending the edges
            signalim = set{theface};
            signalim = signalim - mean2(signalim); %normalize blend stim part 1
            signalim = signalim / std2(signalim); %normalize blend stim part 2
            % imshow(signalim)
            
            toblendim = imset.blend_stim{theface};
            toblendim = toblendim - mean2(toblendim); %normalize blend stim part 1
            toblendim = toblendim / std2(toblendim); %normalize blend stim part 2
            % imshow(toblendim)
            
            % now we're combining the images
            if stimulus == '0'
                combim = toblendim;
            else
                combim = (signalim*signal) + (toblendim*noise);
            end
                % imshow(combim)
            
            % normalising the face pixels of the image
            combim(facepixindex) = combim(facepixindex) - mean2(combim(facepixindex)); %normalize blend stim part 1
            combim(facepixindex) = combim(facepixindex) / std2(combim(facepixindex)); %normalize blend stim part 2
            combim(facepixindex) = (combim(facepixindex)*face_LC(2)) + face_LC(1);
            
            % giving desired lum&contrast to background
            backim = imset.iter_back{theback};
            backim = backim - mean2(backim); %normalize blend stim part 1
            backim = backim / std2(backim); %normalize blend stim part 2
            backim	= (backim*LC(2)) + LC(1);
            % imshow(backim)
            
            % blending the edges
            blendim = backim.*(MaskAlpha) + combim.*(1-MaskAlpha);
            % imshow(blendim)

            fprintf('mean: %f - std: %f - face %d for type: %s blendedddd\n',mean2(blendim),std2(blendim),theface,stimulus) % check contr and lum for the background
            imshow(blendim); pause (0.05)

            imset.blendim{theback,thestim,theface} = blendim;     	

            finalstim_backpixLC{theback,thestim}(theface,:) = [mean(blendim(backpixindex)) std(blendim(backpixindex))]; %%%% $$$$$$
            finalstim_facepixLC{theback,thestim}(theface,:) = [mean(blendim(facepixindex)) std(blendim(facepixindex))]; %%%% $$$$$$

            % saving the stimuli with correct naming
            if strcmp(stimulus,'mask')
                name = [backname '_ID' num2str(theface) '-BB.bmp'];
                imwrite(blendim,[outfolder_mask name],'BMP')
            else
                name = [backname '_ID' num2str(theface) '-' stimulus '.bmp'];
                imwrite(blendim,[outfolder_stim name],'BMP')
            end
            
        end
        imshow(backim); 
        finalbackim_backpixLC{theback,thestim} = [mean(backim(backpixindex)) std(backim(backpixindex))]; %%%% $$$$$$
        finalbackim_facepixLC{theback,thestim} = [mean(backim(facepixindex)) std(backim(facepixindex))] ;%%%% $$$$$$

        imwrite(backim,[outfolder_back backname '.bmp'],'BMP')
    end
end




%%

disp('saving..')
save([basefolder outputmat],'-v7.3')
%load([basefolder outputmat])


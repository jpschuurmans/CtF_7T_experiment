%%
%code for checking luminance and contrast for the stimuli
close all; clear; clc

basefolder = 'C:/Users/Adminuser/Documents/04_CtF-7T/Experiment/stimuli_matlab/';
addpath(basefolder)


load([basefolder 'RPV1_BLEND.mat'])
outfolder_stim = [basefolder 'finalstim/'];

%imset.blendim{theback,thestim,theface}
%inact faces:       imshow(imset.eq_stim{2})
%negated faces:     imshow(imset.neg_stim{1})
%scrambled faces:   imshow(imset.scr_stim{1})
%masks:             imset.mask{thetype,thesf,theim}
%background:        imset.Back_scr{theframe}

outputmat = 'RPV1_CHECK.mat';






%% CHECK plot luminance and contrast
%preallocating
dataStimLback = zeros(backgrounds,length(finalstim_backpixLC(:,1))); dataStimCback = dataStimLback; dataStimLface = dataStimLback; dataStimCface = dataStimLback;
StimLback = zeros(length(stimuli),length(reshape(dataStimCface,numel(dataStimCface),1))); StimLface = StimLback; StimCback =StimLback; StimCface = StimLback;

%thestim = 1; %stim, maskLSF, maskHSF
for thestim = 1:length(stimuli)

    for theback = 1:backgrounds %for all scrambled backgrounds
        dataStimLback(theback,:) = finalstim_backpixLC{theback,thestim}(:,1);
        dataStimCback(theback,:) = finalstim_backpixLC{theback,thestim}(:,2);
        dataStimLface(theback,:) = finalstim_facepixLC{theback,thestim}(:,1);
        dataStimCface(theback,:) = finalstim_facepixLC{theback,thestim}(:,2);
    end

    vecdataStimLback = reshape(dataStimLback,numel(dataStimLback),1);
    vecdataStimLface = reshape(dataStimLface,numel(dataStimLface),1);
    vecdataStimCback = reshape(dataStimCback,numel(dataStimCback),1);
    vecdataStimCface = reshape(dataStimCface,numel(dataStimCface),1);

    StimLback(thestim,:) = vecdataStimLback;
    StimLface(thestim,:) = vecdataStimLface;
    StimCback(thestim,:) = vecdataStimCback;
    StimCface(thestim,:) = vecdataStimCface;
end


close all
colorsc = hsv(length(stimuli));
figure
subplot(2,2,1)
for thestim = 1:length(stimuli) % intact, negated and scrambled
    plot(StimLback(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
title('Luminance of back pixels across images and blocks')
legend('Location','southeast')
legend('mask','75','50','25','0')
ylim ([0.35 0.55])
text(4,0.540,'mask')
text(100,0.540,['mean: ' num2str(mean(StimLback(1,:))) ', std: ' num2str(std(StimLback(1,:)))])
text(4,0.525,'75')
text(100,0.525,['mean: ' num2str(mean(StimLback(2,:))) ', std: ' num2str(std(StimLback(2,:)))])
text(4,0.510,'50')
text(100,0.510,['mean: ' num2str(mean(StimLback(3,:))) ', std: ' num2str(std(StimLback(3,:)))])
text(4,0.495,'25')
text(100,0.495,['mean: ' num2str(mean(StimLback(4,:))) ', std: ' num2str(std(StimLback(4,:)))])
text(4,0.480,'0')
text(100,0.480,['mean: ' num2str(mean(StimLback(5,:))) ', std: ' num2str(std(StimLback(5,:)))])

subplot(2,2,2)
for thestim = 1:length(stimuli) % intact, negated and scrambled
    plot(StimLface(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
ylim ([0.35 0.55])
title('Luminance of face pixels across images and blocks')
text(4,0.540,'mask')
text(100,0.540,['mean: ' num2str(mean(StimLface(1,:))) ', std: ' num2str(std(StimLface(1,:)))])
text(4,0.525,'75')
text(100,0.525,['mean: ' num2str(mean(StimLface(2,:))) ', std: ' num2str(std(StimLface(2,:)))])
text(4,0.510,'50')
text(100,0.510,['mean: ' num2str(mean(StimLface(3,:))) ', std: ' num2str(std(StimLface(3,:)))])
text(4,0.495,'25')
text(100,0.495,['mean: ' num2str(mean(StimLface(4,:))) ', std: ' num2str(std(StimLface(4,:)))])
text(4,0.480,'0')
text(100,0.480,['mean: ' num2str(mean(StimLface(5,:))) ', std: ' num2str(std(StimLface(5,:)))])

subplot(2,2,3)
for thestim = 1:length(stimuli) % intact, negated and scrambled
    plot(StimCback(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
ylim ([0.05 0.16])
title('Contrast of back pixels across images and blocks')
text(4,0.15,'mask')
text(100,0.15,['mean: ' num2str(mean(StimCback(1,:))) ', std: ' num2str(std(StimCback(1,:)))])
text(4,0.1425,'75')
text(100,0.1425,['mean: ' num2str(mean(StimCback(2,:))) ', std: ' num2str(std(StimCback(2,:)))])
text(4,0.1350,'50')
text(100,0.1350,['mean: ' num2str(mean(StimCback(3,:))) ', std: ' num2str(std(StimCback(3,:)))])
text(4,0.1275,'25')
text(100,0.1275,['mean: ' num2str(mean(StimCback(4,:))) ', std: ' num2str(std(StimCback(4,:)))])
text(4,0.12,'0')
text(100,0.12,['mean: ' num2str(mean(StimCback(5,:))) ', std: ' num2str(std(StimCback(5,:)))])


subplot(2,2,4)
for thestim = 1:length(stimuli) % intact, negated and scrambled
    plot(StimCface(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
ylim ([0.05 0.16])
title('Contrast of face pixels across images and blocks')
text(4,0.15,'mask')
text(100,0.15,['mean: ' num2str(mean(StimCface(1,:))) ', std: ' num2str(std(StimCface(1,:)))])
text(4,0.1425,'75')
text(100,0.1425,['mean: ' num2str(mean(StimCface(2,:))) ', std: ' num2str(std(StimCface(2,:)))])
text(4,0.1350,'50')
text(100,0.1350,['mean: ' num2str(mean(StimCface(3,:))) ', std: ' num2str(std(StimCface(3,:)))])
text(4,0.1275,'25')
text(100,0.1275,['mean: ' num2str(mean(StimCface(4,:))) ', std: ' num2str(std(StimCface(4,:)))])
text(4,0.12,'0')
text(100,0.12,['mean: ' num2str(mean(StimCface(5,:))) ', std: ' num2str(std(StimCface(5,:)))])

savename = [outfolder_stim 'Stim_LumContr.png'];
saveas(gcf,savename)



%% do the same for background stimuli
%preallocating
dataBackLback = zeros(backgrounds,length(finalstim_backpixLC(:,1))); dataBackCback = dataBackLback; dataBackLface = dataBackLback; dataBackCface = dataBackLback;
BackLback = zeros(length(stimuli),length(reshape(dataBackCface,numel(dataBackCface),1))); BackLface = BackLback; BackCback =BackLback; BackCface = BackLback;

%thestim = 1; %stim, maskLSF, maskHSF
for thestim = 1:length(stimuli)

    for theback = 1:backgrounds %for all scrambled backgrounds
        dataBackLback(theback,:) = finalbackim_backpixLC{theback,thestim}(:,1);
        dataBackCback(theback,:) = finalbackim_backpixLC{theback,thestim}(:,2);
        dataBackLface(theback,:) = finalbackim_facepixLC{theback,thestim}(:,1);
        dataBackCface(theback,:) = finalbackim_facepixLC{theback,thestim}(:,2);
    end

    vecdataBackLback = reshape(dataBackLback,numel(dataBackLback),1);
    vecdataBackLface = reshape(dataBackLface,numel(dataBackLface),1);
    vecdataBackCback = reshape(dataBackCback,numel(dataBackCback),1);
    vecdataBackCface = reshape(dataBackCface,numel(dataBackCface),1);

    BackLback(thestim,:) = vecdataBackLback;
    BackLface(thestim,:) = vecdataBackLface;
    BackCback(thestim,:) = vecdataBackCback;
    BackCface(thestim,:) = vecdataBackCface;
end


close all
colorsc = hsv(length(stimuli));
figure
subplot(2,2,1)
for thestim = 1:length(stimuli) % mask, 75, 50, 25, 0
    plot(BackLback(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
title('Luminance of back pixels across background images and blocks')
legend('Location','southeast')
legend('mask','75','50','25','0')
ylim ([0.35 0.55])
text(4,0.540,'mask')
text(100,0.540,['mean: ' num2str(mean(BackLback(1,:))) ', std: ' num2str(std(BackLback(1,:)))])
text(4,0.525,'75')
text(100,0.525,['mean: ' num2str(mean(BackLback(2,:))) ', std: ' num2str(std(BackLback(2,:)))])
text(4,0.510,'50')
text(100,0.510,['mean: ' num2str(mean(BackLback(3,:))) ', std: ' num2str(std(BackLback(3,:)))])
text(4,0.495,'25')
text(100,0.495,['mean: ' num2str(mean(BackLback(4,:))) ', std: ' num2str(std(BackLback(4,:)))])
text(4,0.480,'0')
text(100,0.480,['mean: ' num2str(mean(BackLback(5,:))) ', std: ' num2str(std(BackLback(5,:)))])

subplot(2,2,2)
for thestim = 1:length(stimuli) % mask, 75, 50, 25, 0
    plot(BackLface(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
ylim ([0.35 0.55])
title('Luminance of face pixels across background images and blocks')
text(4,0.540,'mask')
text(100,0.540,['mean: ' num2str(mean(BackLface(1,:))) ', std: ' num2str(std(BackLface(1,:)))])
text(4,0.525,'75')
text(100,0.525,['mean: ' num2str(mean(BackLface(2,:))) ', std: ' num2str(std(BackLface(2,:)))])
text(4,0.510,'50')
text(100,0.510,['mean: ' num2str(mean(BackLface(3,:))) ', std: ' num2str(std(BackLface(3,:)))])
text(4,0.495,'25')
text(100,0.495,['mean: ' num2str(mean(BackLface(4,:))) ', std: ' num2str(std(BackLface(4,:)))])
text(4,0.480,'0')
text(100,0.480,['mean: ' num2str(mean(BackLface(5,:))) ', std: ' num2str(std(BackLface(5,:)))])

subplot(2,2,3)
for thestim = 1:length(stimuli) % mask, 75, 50, 25, 0
    plot(BackCback(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
ylim ([0.05 0.16])
title('Contrast of back pixels across background images and blocks')
text(4,0.15,'mask')
text(100,0.15,['mean: ' num2str(mean(BackCback(1,:))) ', std: ' num2str(std(BackCback(1,:)))])
text(4,0.1425,'75')
text(100,0.1425,['mean: ' num2str(mean(BackCback(2,:))) ', std: ' num2str(std(BackCback(2,:)))])
text(4,0.1350,'50')
text(100,0.1350,['mean: ' num2str(mean(BackCback(3,:))) ', std: ' num2str(std(BackCback(3,:)))])
text(4,0.1275,'25')
text(100,0.1275,['mean: ' num2str(mean(BackCback(4,:))) ', std: ' num2str(std(BackCback(4,:)))])
text(4,0.12,'0')
text(100,0.12,['mean: ' num2str(mean(BackCback(5,:))) ', std: ' num2str(std(BackCback(5,:)))])


subplot(2,2,4)
for thestim = 1:length(stimuli) % mask, 75, 50, 25, 0
    plot(BackCface(thestim,:)','-o','Color',colorsc(thestim,:))
    hold on
end
ylim ([0.05 0.16])
title('Contrast of face pixels across background images and blocks')
text(4,0.15,'mask')
text(100,0.15,['mean: ' num2str(mean(BackCface(1,:))) ', std: ' num2str(std(BackCface(1,:)))])
text(4,0.1425,'75')
text(100,0.1425,['mean: ' num2str(mean(BackCface(2,:))) ', std: ' num2str(std(BackCface(2,:)))])
text(4,0.1350,'50')
text(100,0.1350,['mean: ' num2str(mean(BackCface(3,:))) ', std: ' num2str(std(BackCface(3,:)))])
text(4,0.1275,'25')
text(100,0.1275,['mean: ' num2str(mean(BackCface(4,:))) ', std: ' num2str(std(BackCface(4,:)))])
text(4,0.12,'0')
text(100,0.12,['mean: ' num2str(mean(BackCface(5,:))) ', std: ' num2str(std(BackCface(5,:)))])

savename = [outfolder_stim 'Back_LumContr.png'];
saveas(gcf,savename)

## Light Intensity on sleep quality

### Introduction

The increase of artificial light exposure through the increased prevalence of technology has an affect on the sleep cycle and circadian rhythm of humans. The goal of this project is to determine how different colors and intensities of light exposure prior to sleep affects the quality of sleep through the classification of time series data. 

### Background Information

As the world undergoes technological advancement on an unprecedented scale, artificial light from man-made sources is becoming ever more prevalent. The extent of this anthropogenic increase in artificial light has become a pollutant, with extensive research showing both ecological and medical consequences [1]. This is due to the importance of light from the sun on the survival and function of the majority of organisms and thus ecosystems on earth. These organisms have developed day/night cycles that cause physiological, behavioral, and metabolic changes which optimize function and are essential for survival. Artificial light interferes with these processes due to differences in wavelength, intensity, and timing from that of light with origins from the sun. A study of satellite images done in 2001, showed that artificial light at night (ALAN) affects 18.7% of global land area , through which roughly two-thirds of the human population and 99% of humans living in the United States and the European Union, “live in areas where the night sky is above the threshold set for polluted status.” [2] The rapid development of technology and thus a rapid increase in artificial light within the last two hundred years has undoubtedly had effects on the biological function of organisms around the world.

![image](https://user-images.githubusercontent.com/46830657/156947468-01a1c61e-f3b3-4166-a34b-cbec47b72c7f.png)

What is most concerning for the health of humans, however, is the ever-increasing use of devices with light-up displays such as phones, TVs, and computers for entertainment, work, and communication. Currently, there are an estimated 16 billion mobile devices worldwide [3] with many individuals spending over five hours a day looking at a screen. One biological mechanism that is affected by this increased exposure to artificial light in human beings is the circadian rhythm, through which the body undergoes changes during the night in preparation for sleep and changes during the day in preparation for activity. The circadian rhythm plays major roles in many “physiological processes, such as body temperature, blood pressure, hormone secretion, gene expression, and immune functions” [4], which all have some reliance on diurnal light patterns from the sun and thus the optimized function of these human body processes are impacted by stimulus from artificial sources of light. When light enters the eyes and is picked up by photosensitive ganglion cells, this information is then communicated to the suprachiasmatic nuclei of the hypothalamus, and then to other parts of the brain and body. One result is that the brain experiences an increase in wakefulness and reduction in homeostatic sleep pressure in the presence of light [5] through the suppression of melatonin, a hormone released by the pineal gland which facilitates sleep and the circadian rhythm. 

 ![image](https://user-images.githubusercontent.com/46830657/156948045-9edc7794-e503-419d-9c6e-5693a9c71495.png)
 
As a result light exposure during unnatural times can detrimentally affect sleep, which is necessary for human health and function. Sleep deprivation or impairment can lead to many health issues such as impairment to cognition [6], metabolism [7], and immune response [8]. This leads to the focus of this project, which is to determine the effects of light exposure on sleep quality.

### Data
The data used in this project comes from the Sueño Ancillary study done by The Hispanic Community Health Study / Study of Latinos (HCHS/SOL). The data is composed of wrist-worn actimetry sensor data taken over the course of one week for each participant (n=2252). Measurements are taken from the sensor in thirty-second intervals and consist of blue, green, red, and white light intensities, locomotor activity, time, and sleep interval indicators [9]. One notable feature that we use is the interval indicator, which describes whether the patient is asleep, awake or resting for a given epoch. This uses the study’s sleep/wake detection algorithm to determine.


![image](https://user-images.githubusercontent.com/46830657/157585465-e7683746-5a5c-4a01-a79f-d8ff56efaa51.png)

### Methods
The outcome variable that we used for the data is sleep efficiency which is defined by the ratio between the duration of time the participant spent sleeping over the duration of time spent in bed for a given night. We defined a "good" sleep as one where at least 95% of the time spent is bed is actual sleep. The sleep efficiency equation is shown below:

![image](https://user-images.githubusercontent.com/46830657/156948066-09b1a1f8-c9bb-41da-8336-2f682d9a8e29.png)

#### ROCKET Classifier


#### LSTM(RNN)


### Bibliography
[1] Gaston, K. J., Bennie, J., Davies, T. W., &amp; Hopkins, J. (2013). The ecological impacts of nighttime light pollution: A mechanistic appraisal. Biological Reviews, 88(4), 912–927. https://doi.org/10.1111/brv.12036 

[2] P. Cinzano, F. Falchi, C.D. Elvidge, The first World Atlas of the artificial night sky brightness, Monthly Notices of the Royal Astronomical Society, Volume 328, Issue 3, December 2001, Pages 689–707, https://doi.org/10.1046/j.1365-8711.2001.04882.x

[3] Published by S. O'Dea, S. O. D. (2021, September 24). Number of mobile devices worldwide 2020-2025. Statista. Retrieved March 4, 2022, from https://www.statista.com/statistics/245501/multiple-mobile-device-ownership-worldwide/ 

[4] Cable, J., Schernhammer, E., Hanlon, E. C., Vetter, C., Cedernaes, J., Makarem, N., Dashti, H. S., Shechter, A., Depner, C., Ingiosi, A., Blume, C., Tan, X., Gottlieb, E., Benedict, C., Van Cauter, E., &amp; St‐Onge, M. P. (2021). Sleep and circadian rhythms: Pillars of Health—a keystone symposia report. Annals of the New York Academy of Sciences, 1506(1), 18–34. https://doi.org/10.1111/nyas.14661 

[5] Rahman SA, Flynn-Evans EE, Aeschbach D, Brainard GC, Czeisler CA, Lockley SW. Diurnal spectral sensitivity of the acute alerting effects of light. Sleep. 2014 Feb 1;37(2):271-81. doi: 10.5665/sleep.3396. PMID: 24501435; PMCID: PMC3900613.

[6] Killgore, W. D. S. (2010). Effects of sleep deprivation on cognition. Progress in Brain Research, 105–129. https://doi.org/10.1016/b978-0-444-53702-7.00007-5 

[7] Knutson, K. L., Spiegel, K., Penev, P., &amp; Van Cauter, E. (2007). The metabolic consequences of sleep deprivation. Sleep Medicine Reviews, 11(3), 163–178. https://doi.org/10.1016/j.smrv.2007.01.002 

[8] Spiegel K, Sheridan JF, Van Cauter E. Effect of Sleep Deprivation on Response to Immunization. JAMA. 2002;288(12):1471–1472. doi:10.1001/jama.288.12.1469

[9] Patel SR, Weng J, Rueschman M, Dudley KA, Loredo JS, Mossavar-Rahmani Y, Ramirez M, Ramos AR, Reid K, Seiger AN, Sotres-Alvarez D, Zee PC, Wang R. Reproducibility of a Standardized Actigraphy Scoring Algorithm for Sleep in a US Hispanic/Latino Population. Sleep. 2015 Sep 1;38(9):1497-503. 



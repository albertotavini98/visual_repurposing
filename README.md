# visual_repurposing
This is a python repository with some code i developed for "visual repurposing", an algorithmic equivalent of what pop art exponents used to do: combine pieces of already existing art to create new art. It is meant to extract pieces of pictures and combine them on a background as to create visually stimulating images.  

Here you can find some video edits i created with the generated images:   
Random:   
https://youtube.com/shorts/y3PHcIbA6dc?feature=share  
https://youtube.com/shorts/eanKiusmeQI?feature=share  
https://youtube.com/shorts/Ffv_EbCxHVQ?feature=share    (Berserk inspired)  
Ordered:  
https://youtube.com/shorts/hMBZs5K-eFo?feature=share    
https://youtube.com/shorts/THFb6vlu92Y?feature=share   (Westworld inspired)


There is also an application of K-means clustering as to group the pieces that we then glue to the background chromatically speaking. We use the average on the RGB channels as three features for clustering input.  
Here you can see a plotting of results of a clustering and the corresponding ordered image fragments.

![Image not available!](readme_images/clustering_plot.png)
![Image not available!](readme_images/output.png)

Here an example of RGB channel mixing from different sources (see use_RGB_forge.ipynb):

![Image not available!](readme_images/channel_messing.png)



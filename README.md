# Visual Repurposing
This is a python repository meant to perform "visual repurposing", an algorithmic equivalent of what pop art exponents used to do: combine pieces of already existing art to create new art. It is meant to extract pieces of pictures and combine them on a background as to create visually stimulating images.  

There is also a notebook to automatically sync the images to an audio track and create edits with the pieces. Here you can see some of the results:
Random:   
https://youtube.com/shorts/y3PHcIbA6dc?feature=share  
https://youtube.com/shorts/eanKiusmeQI?feature=share  
https://youtube.com/shorts/Ffv_EbCxHVQ?feature=share    (Berserk inspired)  
Ordered:  
https://youtube.com/shorts/hMBZs5K-eFo?feature=share    
https://youtube.com/shorts/THFb6vlu92Y?feature=share   (Westworld inspired)


There is also an application of K-means clustering as to group the pieces that we then glue to the background. We use the average on the RGB channels as three features for clustering input.  
Here you can see a plotting of results of a clustering and the corresponding ordered image fragments.

![Image not available!](readme_images/clustering_plot.png)
![Image not available!](readme_images/output.png)

I also messed around with RGB channels of images, creating pieces like: 

![Image not available!](readme_images/channel_messing.png)



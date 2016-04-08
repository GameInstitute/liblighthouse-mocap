# liblighthouse-mocap
Lighthouse Mocap is an open source motion capture library designed to record positional data using Valve's Lighthouse tracking system.

# How Lighthouse Works
Since there are still quiet a few posts/comments which take false assumptions about how the tracking system from htc's vive works here is an explanation with illustrations:

**1st:** lighthouse stations are passive. They just need power to work. There is no radio signal between the lighthouse boxes and the vive or pc. (However the lighthouse stations can communicate via radio signals for syncronization purposes)    

**2nd:** The lighthouse boxes work literally just like lighthouses in maritime navigation: they send out (for humans invisible infrared) light signals which then the vive's IR-diodes can see. Here's a gif from gizmodo where you can see an early prototype working:     
![](http://i.kinja-img.com/gawker-media/image/upload/s--wsP3xmPN--/1259287828241194666.gif)

**3rd:** Three different signals are sent from the lighthouse boxes: At first they send a omnidirectional flash. This flash is send syncronous from both stations and purposes to the vive (or vives controllers) as a "start now to trigger a stopwatch"-command. Then each station transmitts two IR-laser swipes consecutivelay - much like a 'scanning line' through the room. One swipe is sent horizontally the other one after that is transmitted vertically.    

**4th:** The vives's IR-Diodes register the laser swipes on different times due to the speed of the angular motion of the swipe. With the help of these (tiny) time differences between the flash and the swipes and also because of the fixed and know position of the IR-diodes on the vive's case, the exact position and orientation can be calculated. This video on youtube illustrates the process pretty good: ["HTC Vive Lighthouse Chaperone tracking system Explained"](https://youtu.be/J54dotTt7k0)

**5th:** the calculated position/orientations are sent to the pc along with other position relevant sensory data.

### Whats the benefit of this system compared to others?  

-the lighthouse boxes are dumb. Their components are simple and cheap.  

-they don't need a high bandwith connection to any of the VR systems's components (headset or pc).  

-tracking resolution is not limited or narrowed down to the camera resolution like on conventional solutions.  

-sub millimeter tracking is possible with 60 Hz even from 2+ m distances (with cameras the resolution goes down when you step away from the sensor).  

-position/orientation calculations are fast and easy handable by (more) simple CPUs/micro controllers. No image processing cpu time is consumed like on camera based solutions.  

-to avoid occlusion, multiple lighthouses can be installed without the need to process another hi-res/hi-fps camera signal.

[source](https://www.reddit.com/r/Vive/comments/40877n/vive_lighthouse_explained/)

# M5 part 3

---

## Define

key points of sucess:
- latency
- ease of use/very intuitive

## Measurement

Latency:
- latency is key aspect to consider when sending data over a network
- M4 players see noticeable lag when moving the paddle given the acceleration of the Y axis
- Since M4 considers absolute mappings of the acceleration to the postion of the board, movement to a certain position is accompanied up to 20 frames of lag until the update
    - Here is an example (where it prints a pair of data in two lines, in this example 15 frames of lag)
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
    173.4
    -16.32
---

- M5 on the other hand also has the same latency but since it is not absolute mapped, the latency is not as noticeable
- In M5, there is a bit of lag (up to 15 frames) in the beginning and ending of each movement but since the paddle traverses a wider range, the lag in not noticeable

## Ease of Use
- Subjects found that mapping the paddle movement to acceleration was very intuitive
- a simple twist allow users to move the paddle


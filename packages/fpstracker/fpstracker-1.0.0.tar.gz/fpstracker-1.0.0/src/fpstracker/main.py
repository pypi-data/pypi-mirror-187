import cv2
import time

class Tracker:

    previous_time = 0

    average_fps = "..."

    avgfps = []

    initial_time =time.time()

    def FPS(self, img, pos1 = (10,25), Average_FPS = True, pos2 = (420,25)):

        current_time = time.time()

        fps = int(1/(current_time - self.previous_time))

        self.avgfps.append(fps)

        self.previous_time = current_time

        timer = time.time() - self.initial_time

        if timer > 5:
            self.average_fps = int(sum(self.avgfps)/len(self.avgfps))
            self.initial_time = time.time()
        
        cv2.putText(img, f"FPS : {fps}", pos1, cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
        if Average_FPS:
            cv2.putText(img, f"Avg FPS : {self.average_fps}", pos2, cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
        
        return img
from hamamatsu.dcam import copy_frame, dcam, Stream
import logging
import matplotlib.pyplot as plt
import time

def gen_acquire(device, exposure_time=1, nb_frames=1):
    """Simple acquisition example"""
    device["exposure_time"] = exposure_time
    with Stream(device, nb_frames) as stream:
        logging.info("start acquisition")
        device.start()
        for frame in stream:
            yield copy_frame(frame)
        logging.info("finised acquisition")

def main(args=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nb-frames", default=1, type=int)
    parser.add_argument("-e", "--exposure-time", default=0.1, type=float)
    parser.add_argument(
        "--log-level",
        help="log level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARN", "ERROR"],
    )
    options = parser.parse_args(args)
    log_fmt = "%(levelname)s %(asctime)-15s %(name)s: %(message)s"
    logging.basicConfig(level=options.log_level.upper(), format=log_fmt)

    with dcam:
        with dcam[0] as camera:
            for i, frame in enumerate(
                gen_acquire(camera, options.exposure_time, options.nb_frames)
            ):
                logging.info(
                    f"Frame #{i+1}/{options.nb_frames} {frame.shape} {frame.dtype}"
                )
                plt.imshow(frame, cmap='gray')
                plt.show()


def get_camera():
    with dcam:
        with dcam[0] as camera:
            return camera

def get_image(cam, exposure_time=0.1, nb_frames=1):
    for i, frame in enumerate(
        gen_acquire(cam, exposure_time, nb_frames)
    ):
        return frame


if __name__ == "__main__":
    cam = get_camera()
    for i in range(3):
        frame = get_image(cam)

    plt.imshow(frame, cmap='gray')
    plt.show()
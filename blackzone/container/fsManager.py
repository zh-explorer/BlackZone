import ctypes
import os


class FsManager(object):
    def __init__(self, image_id, container_id, cwd="/home/explorer/mycontainer/"):
        libc = ctypes.cdll.LoadLibrary("libc.so.6")
        self.__mount = libc.mount
        self.__umount = libc.umount

        image_dir = os.path.join(cwd, "image", image_id)
        if not os.path.isdir(image_dir):
            raise IOError("image is not exists", image_dir)

        container_main_dir = os.path.join(cwd, "container")
        if not os.path.exists(container_main_dir):
            os.mkdir(container_main_dir, 755)
        elif os.path.isfile(container_main_dir):
            raise IOError("container dir is not a dir", container_main_dir)

        container_dir = os.path.join(container_main_dir, container_id)
        if not os.path.exists(container_dir):
            os.mkdir(container_dir, 0755)
        elif os.path.isfile(container_dir):
            raise IOError("container dir is not a dir", container_dir)

        rootfs = os.path.join(container_dir, "rootfs")
        if not os.path.exists(rootfs):
            os.mkdir(rootfs, 0755)
        elif os.path.isfile(rootfs):
            raise IOError("rootfs dir is a file", rootfs)

        self.rootfs = rootfs
        self.image_dir = image_dir
        self.container_dir = container_dir

    def mount_aufs(self):
        self.check_permission()

        result = self.__mount("none", self.rootfs, "aufs", 0, "br:%s=rw:%s=ro" % (self.rootfs, self.image_dir))
        if result != 0:
            raise OSError("mount failed:", result)

    def umount_fs(self):
        self.check_permission()
        if os.path.ismount(self.rootfs):
            result = self.__umount(self.rootfs, 0)
            if result != 0:
                raise OSError("mount failed:", result)

    def clean_container(self):
        self.umount_fs()
        for root, dirs, files in os.walk(self.container_dir, topdown=False):
            for f in files:
                p = os.path.join(root, f)
                os.unlink(p)
            os.rmdir(root)

    @staticmethod
    def check_permission():
        if os.getuid() != 0:
            raise OSError("cannot mount: Permission denied")

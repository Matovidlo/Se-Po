# This module was created by Martin Vasko
# It contains all prescribed templates for different build systems such as
# gradle, maven xml, xml or any other, vagranfile templates for Windows
# and CentOS. Also includes eddited seccomp profile without networking

seccomp_without_network = """
{
    "defaultAction": "SCMP_ACT_ERRNO",
    "architectures": [
        "SCMP_ARCH_X86_64",
        "SCMP_ARCH_X86",
        "SCMP_ARCH_X32"
    ],
    "syscalls": [
        {
            "name": "access",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "alarm",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "brk",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "capget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "capset",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "chdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "clock_getres",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "clock_gettime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "clock_nanosleep",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "close",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "copy_file_range",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "creat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "dup",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "dup2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "dup3",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_create1",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_ctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_ctl_old",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_pwait",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_wait",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "epoll_wait_old",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "eventfd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "eventfd2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "execve",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "execveat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "exit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "exit_group",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "faccessat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fadvise64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fadvise64_64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fallocate",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fanotify_mark",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchmodat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fchownat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fcntl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fcntl64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fdatasync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fgetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "flistxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "flock",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fork",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fremovexattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fsetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstatat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstatfs",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fstatfs64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "fsync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ftruncate",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ftruncate64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "futex",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "futimesat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getcpu",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getcwd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getdents",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getdents64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getegid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getegid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "geteuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "geteuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgroups",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getgroups32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getitimer",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpeername",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpgrp",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getppid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getpriority",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getrandom",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getresuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getrlimit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "get_robust_list",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getrusage",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getsid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "get_thread_area",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "gettid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "gettimeofday",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "getxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_add_watch",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_init",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_init1",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "inotify_rm_watch",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_cancel",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ioctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_destroy",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_getevents",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ioprio_get",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ioprio_set",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_setup",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "io_submit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ipc",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "kill",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lgetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "link",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "linkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "listxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "llistxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "_llseek",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lremovexattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lseek",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lsetxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lstat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "lstat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "madvise",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "memfd_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mincore",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mkdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mkdirat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mknod",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mknodat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mmap",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mmap2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mprotect",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_getsetattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_notify",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_open",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_timedreceive",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_timedsend",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mq_unlink",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "mremap",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgrcv",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msgsnd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "msync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "munlock",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "munlockall",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "munmap",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "nanosleep",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "newfstatat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "_newselect",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "open",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "openat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pause",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pipe",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pipe2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "poll",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ppoll",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "prctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pread64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "preadv",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "prlimit64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pselect6",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pwrite64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "pwritev",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "read",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readahead",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readlink",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readlinkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "readv",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "remap_file_pages",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "removexattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rename",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "renameat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "renameat2",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "restart_syscall",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rmdir",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigaction",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigpending",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigprocmask",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigqueueinfo",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigreturn",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigsuspend",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_sigtimedwait",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "rt_tgsigqueueinfo",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getaffinity",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getparam",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_get_priority_max",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_get_priority_min",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_getscheduler",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_rr_get_interval",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setaffinity",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setparam",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_setscheduler",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sched_yield",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "seccomp",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "select",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semop",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "semtimedop",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "send",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sendfile",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sendfile64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setfsuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgroups",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setgroups32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setitimer",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setpgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setpriority",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setregid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setregid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresgid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresgid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setresuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setreuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setreuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setrlimit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "set_robust_list",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setsid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setsockopt",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "set_thread_area",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "set_tid_address",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setuid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setuid32",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "setxattr",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmdt",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shmget",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "shutdown",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sigaltstack",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "signalfd",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "signalfd4",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sigreturn",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "splice",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "stat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "stat64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "statfs",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "statfs64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "symlink",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "symlinkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sync",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "sync_file_range",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "syncfs",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "syslog",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "tee",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "tgkill",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "time",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_delete",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timerfd_create",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timerfd_gettime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timerfd_settime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_getoverrun",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_gettime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "timer_settime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "times",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "tkill",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "truncate",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "truncate64",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "ugetrlimit",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "umask",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "unlinkat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "utime",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "utimensat",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "utimes",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "vfork",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "vmsplice",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "wait4",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "waitid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "waitpid",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "write",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "writev",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "arch_prctl",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        },
        {
            "name": "modify_ldt",
            "action": "SCMP_ACT_ALLOW",
            "args": []
        }
    ]
}
"""

kotlin_gradle = """
buildscript {
    repositories {
        jcenter()
    }
}

plugins {
    id("io.gitlab.arturbosch.detekt").version("1.10.0")
}

repositories {
    jcenter()
}
"""
requirements_txt = """

"""

Gemfile = """
source 'https://rubygems.org' do
  # Gems here
  {}
end
"""

composer_json = """
{{
    \"require\": {{
{packages}
    }}
}}
"""

Cargo_toml = """
[dependencies]
rustfix = "0.5.1"
"""

eslint = """
{
  "parserOptions": {
    "ecmaVersion": 2020,
    "ecmaFeatures": {
      "jsx": true
    },
    "sourceType": "module"
  },

  "env": {
    "es6": true,
    "node": true
  },

  "plugins": [
    "import",
    "node",
    "promise",
    "standard"
  ],

  "globals": {
    "document": "readonly",
    "navigator": "readonly",
    "window": "readonly"
  },

  "rules": {
    "accessor-pairs": "error",
    "array-bracket-spacing": ["error", "never"],
    "arrow-spacing": ["error", { "before": true, "after": true }],
    "block-spacing": ["error", "always"],
    "brace-style": ["error", "1tbs", { "allowSingleLine": true }],
    "camelcase": ["error", { "properties": "never" }],
    "comma-dangle": ["error", {
      "arrays": "never",
      "objects": "never",
      "imports": "never",
      "exports": "never",
      "functions": "never"
    }],
    "comma-spacing": ["error", { "before": false, "after": true }],
    "comma-style": ["error", "last"],
    "computed-property-spacing": ["error", "never"],
    "constructor-super": "error",
    "curly": ["error", "multi-line"],
    "dot-location": ["error", "property"],
    "dot-notation": ["error", { "allowKeywords": true }],
    "eol-last": "error",
    "eqeqeq": ["error", "always", { "null": "ignore" }],
    "func-call-spacing": ["error", "never"],
    "generator-star-spacing": ["error", { "before": true, "after": true }],
    "handle-callback-err": ["error", "^(err|error)$" ],
    "indent": ["error", 2, {
      "SwitchCase": 1,
      "VariableDeclarator": 1,
      "outerIIFEBody": 1,
      "MemberExpression": 1,
      "FunctionDeclaration": { "parameters": 1, "body": 1 },
      "FunctionExpression": { "parameters": 1, "body": 1 },
      "CallExpression": { "arguments": 1 },
      "ArrayExpression": 1,
      "ObjectExpression": 1,
      "ImportDeclaration": 1,
      "flatTernaryExpressions": false,
      "ignoreComments": false,
      "ignoredNodes": ["TemplateLiteral *"]
    }],
    "key-spacing": ["error", { "beforeColon": false, "afterColon": true }],
    "keyword-spacing": ["error", { "before": true, "after": true }],
    "lines-between-class-members": ["error", "always", { "exceptAfterSingleLine": true }],
    "new-cap": ["error", { "newIsCap": true, "capIsNew": false, "properties": true }],
    "new-parens": "error",
    "no-array-constructor": "error",
    "no-async-promise-executor": "error",
    "no-caller": "error",
    "no-case-declarations": "error",
    "no-class-assign": "error",
    "no-compare-neg-zero": "error",
    "no-cond-assign": "error",
    "no-const-assign": "error",
    "no-constant-condition": ["error", { "checkLoops": false }],
    "no-control-regex": "error",
    "no-debugger": "error",
    "no-delete-var": "error",
    "no-dupe-args": "error",
    "no-dupe-class-members": "error",
    "no-dupe-keys": "error",
    "no-duplicate-case": "error",
    "no-empty-character-class": "error",
    "no-empty-pattern": "error",
    "no-eval": "error",
    "no-ex-assign": "error",
    "no-extend-native": "error",
    "no-extra-bind": "error",
    "no-extra-boolean-cast": "error",
    "no-extra-parens": ["error", "functions"],
    "no-fallthrough": "error",
    "no-floating-decimal": "error",
    "no-func-assign": "error",
    "no-global-assign": "error",
    "no-implied-eval": "error",
    "no-inner-declarations": ["error", "functions"],
    "no-invalid-regexp": "error",
    "no-irregular-whitespace": "error",
    "no-iterator": "error",
    "no-labels": ["error", { "allowLoop": false, "allowSwitch": false }],
    "no-lone-blocks": "error",
    "no-misleading-character-class": "error",
    "no-prototype-builtins": "error",
    "no-useless-catch": "error",
    "no-mixed-operators": ["error", {
      "groups": [
        ["==", "!=", "===", "!==", ">", ">=", "<", "<="],
        ["&&", "||"],
        ["in", "instanceof"]
      ],
      "allowSamePrecedence": true
    }],
    "no-mixed-spaces-and-tabs": "error",
    "no-multi-spaces": "error",
    "no-multi-str": "error",
    "no-multiple-empty-lines": ["error", { "max": 1, "maxEOF": 0 }],
    "no-negated-in-lhs": "error",
    "no-new": "error",
    "no-new-func": "error",
    "no-new-object": "error",
    "no-new-require": "error",
    "no-new-symbol": "error",
    "no-new-wrappers": "error",
    "no-obj-calls": "error",
    "no-octal": "error",
    "no-octal-escape": "error",
    "no-path-concat": "error",
    "no-proto": "error",
    "no-redeclare": ["error", { "builtinGlobals": false }],
    "no-regex-spaces": "error",
    "no-return-assign": ["error", "except-parens"],
    "no-self-assign": ["error", { "props": true }],
    "no-self-compare": "error",
    "no-sequences": "error",
    "no-shadow-restricted-names": "error",
    "no-sparse-arrays": "error",
    "no-tabs": "error",
    "no-template-curly-in-string": "error",
    "no-this-before-super": "error",
    "no-throw-literal": "error",
    "no-trailing-spaces": "error",
    "no-undef": "error",
    "no-undef-init": "error",
    "no-unexpected-multiline": "error",
    "no-unmodified-loop-condition": "error",
    "no-unneeded-ternary": ["error", { "defaultAssignment": false }],
    "no-unreachable": "error",
    "no-unsafe-finally": "error",
    "no-unsafe-negation": "error",
    "no-unused-expressions": ["error", { "allowShortCircuit": true, "allowTernary": true, "allowTaggedTemplates": true }],
    "no-unused-vars": ["error", { "vars": "all", "args": "none", "ignoreRestSiblings": true }],
    "no-use-before-define": ["error", { "functions": false, "classes": false, "variables": false }],
    "no-useless-call": "error",
    "no-useless-computed-key": "error",
    "no-useless-constructor": "error",
    "no-useless-escape": "error",
    "no-useless-rename": "error",
    "no-useless-return": "error",
    "no-void": "error",
    "no-whitespace-before-property": "error",
    "no-with": "error",
    "object-curly-newline": ["error", { "multiline": true, "consistent": true }],
    "object-curly-spacing": ["error", "always"],
    "object-property-newline": ["error", { "allowMultiplePropertiesPerLine": true }],
    "one-var": ["error", { "initialized": "never" }],
    "operator-linebreak": ["error", "after", { "overrides": { "?": "before", ":": "before", "|>": "before" } }],
    "padded-blocks": ["error", { "blocks": "never", "switches": "never", "classes": "never" }],
    "prefer-const": ["error", {"destructuring": "all"}],
    "prefer-promise-reject-errors": "error",
    "quote-props": ["error", "as-needed"],
    "quotes": ["error", "single", { "avoidEscape": true, "allowTemplateLiterals": false }],
    "rest-spread-spacing": ["error", "never"],
    "semi": ["error", "never"],
    "semi-spacing": ["error", { "before": false, "after": true }],
    "space-before-blocks": ["error", "always"],
    "space-before-function-paren": ["error", "always"],
    "space-in-parens": ["error", "never"],
    "space-infix-ops": "error",
    "space-unary-ops": ["error", { "words": true, "nonwords": false }],
    "spaced-comment": ["error", "always", {
      "line": { "markers": ["*package", "!", "/", ",", "="] },
      "block": { "balanced": true, "markers": ["*package", "!", ",", ":", "::", "flow-include"], "exceptions": ["*"] }
    }],
    "symbol-description": "error",
    "template-curly-spacing": ["error", "never"],
    "template-tag-spacing": ["error", "never"],
    "unicode-bom": ["error", "never"],
    "use-isnan": "error",
    "valid-typeof": ["error", { "requireStringLiterals": true }],
    "wrap-iife": ["error", "any", { "functionPrototypeMethods": true }],
    "yield-star-spacing": ["error", "both"],
    "yoda": ["error", "never"],

    "import/export": "error",
    "import/first": "error",
    "import/no-absolute-path": ["error", { "esmodule": true, "commonjs": true, "amd": false }],
    "import/no-duplicates": "error",
    "import/no-named-default": "error",
    "import/no-webpack-loader-syntax": "error",

    "node/no-deprecated-api": "error",
    "node/process-exit-as-throw": "error",

    "promise/param-names": "error",

    "standard/no-callback-literal": "error"
  }
}
"""

vagrant_windows_config = """
Vagrant.configure("2") do |config|
    # Change vm box based on the needs in teplate_build_files.py
    config.vm.box = "gusztavvargadr/windows-10"
    config.vm.hostname = "winsecpovm"
    config.vm.post_up_message = "{msg}"
    config.vm.box_check_update = true
    # Change IP address in case of colission in installed
    # template_build_files.py
    config.vm.network "private_network", ip: "172.168.67.89"

    config.vm.communicator = "winrm"
    # Synced folder where results will be recieved
    config.vm.synced_folder "{sync_folder}", "C:/Users/vagrant/portability_testing", owner:'vagrant', mount_options: ["dmode=775,fmode=644"]

    # In case of wrong provider please change it in teplate_build_files.py
    config.vm.provider "virtualbox" do |vb|
        vb.name = '{name}'
        vb.memory = "2048"
        vb.cpus = "2"
    end
    # Here will be paste commands including tools that are necessary to install.
    config.vm.provision "shell", privileged: "true", inline: <<-'POWERSHELL'
        Set-TimeZone "Coordinated Universal Time"
        # Install Boxstarter
        . {{ iwr -useb https://boxstarter.org/bootstrapper.ps1 }} | iex; Get-Boxstarter -Force
     
        # Copy setup.ps1 to the Temp directory and then run boxstarter with our setup.ps1 script        
        $env:PSModulePath = "$([System.Environment]::GetEnvironmentVariable('PSModulePath', 'User'));$([System.Environment]::GetEnvironmentVariable('PSModulePath', 'Machine'))"
        cp C:/Users/vagrant/portability_testing/setup.ps1 $env:TEMP
        Import-Module Boxstarter.Chocolatey
        $credential = New-Object System.Management.Automation.PSCredential("vagrant", (ConvertTo-SecureString "vagrant" -AsPlainText -Force))
        Install-BoxstarterPackage $env:TEMP\\setup.ps1 -Credential $credential

{cmds}
      POWERSHELL
end
"""

setup_ps1="""
choco install -y 7zip
choco install -y notepadplusplus
# choco install git -y -params '"/GitAndUnixToolsOnPath /NoAutoCrlf"'
choco install -y {tools} --pre
"""

vagrant_centos_config = """
Vagrant.configure("2") do |config|
    # Change vm box based on the needs in teplate_build_files.py
    config.vm.box = "centos/7"
    config.vm.hostname = "secpovm"
    config.vm.post_up_message = "{msg}"
    config.vm.box_check_update = true
    # Change IP address in case of colission in installed
    # template_build_files.py
    config.vm.network "private_network", ip: "172.168.67.89"
    
    # Synced folder where results will be recieved
    config.vm.synced_folder "{sync_folder}", "/home/vagrant/portability_testing"
   
    # In case of wrong provider please change it in teplate_build_files.py
    config.vm.provider "virtualbox" do |vb|
        vb.name = '{name}'
        vb.memory = "2048"
        vb.cpus = "2"
    end
    # Here will be paste commands including tools that are necessary to install.
    config.vm.provision "shell", inline: <<-SHELL
        yum update -y
        yum install -y {tools}
{cmds}
    SHELL
    
end
"""

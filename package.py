#!/usr/bin/env python3

import argparse
import tarfile

from packager.path_chdir import Chdir
from packager.xcode import Xcode


def package_platforms(requested_platforms):
    version = Xcode.version()
    output_file = f'AppleSDK_Xcode{version}.xz'

    print(f'Xcode {version}')

    requested_platforms.sort()
    print(f'Requested platforms: {", ".join(requested_platforms)}')
    available = Xcode.available_platforms()
    missing = set(requested_platforms) - set(available)
    package_platforms = list(set(requested_platforms) - missing)
    package_platforms.sort()

    with tarfile.open(output_file, mode='w:xz') as t:
        for p in package_platforms:
            print(f'Packaging platform: {Xcode.platform_short_name(p)}, version: {Xcode.platform_version(p)}')
            with Chdir(Xcode.platforms_path()):
                t.add(f'./{Xcode.platform_short_name(p)}.platform/Developer/SDKs')

        # print(f'Packaging: XcodeDefault.xctoolchain')
        # with Chdir(Xcode.toolchains_path()):
        #     t.add(f'{Xcode.default_toolchain}/usr/include/c++')

    print(f'Wrote: {output_file}')


def main():
    available_platforms = Xcode.available_platforms()

    parser = argparse.ArgumentParser(description='Package the Xcode SDKs')
    parser.add_argument('--platform', action='append', dest='platforms',
                        help='Specify the SDKs to package, otherwise package all available SDKs')
    parser.add_argument('xip', metavar='XIP', help='Path to the Xcode xip archive')

    args = parser.parse_args()
    if args.platforms:
        platforms = args.platforms
    else:
        platforms = available_platforms

    package_platforms(platforms)


if __name__ == '__main__':
    main()


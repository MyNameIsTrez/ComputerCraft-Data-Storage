#!/bin/sh
set -e
cd "$(dirname "$(realpath "$0")")/src"
dotnet build
../BizHawk/EmuHawkMono.sh --mono-no-redirect --open-ext-tool-dll=MyTool
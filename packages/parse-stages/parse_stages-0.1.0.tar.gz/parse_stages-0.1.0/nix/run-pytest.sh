#!/bin/sh
#
# Copyright (c) Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

set -e

cleanpy()
{
	find . -mindepth 1 -maxdepth 1 -type d \( \
		-name '.tox' \
		-or -name '.mypy_cache' \
		-or -name '.pytest_cache' \
		-or -name '.nox' \
		-or -name '.ruff_cache' \
	\) -exec rm -rf -- '{}' +
	find . -type d -name '__pycache__' -exec rm -rfv -- '{}' +
	find . -type f -name '*.pyc' -delete -print
	find . -mindepth 1 -maxdepth 2 -type d -name '*.egg-info' -exec rm -rfv -- '{}' +
}

for pyver in 38 39 310 311 312; do
	cleanpy
	printf -- '\n===== Running tests for %s\n\n\n' "$pyver"
	nix-shell --pure --arg py-ver "$pyver" nix/python-pytest.nix
	printf -- '\n===== Done with %s\n\n' "$pyver"
done

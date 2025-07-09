# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

ARG AWS_REGION=us-east-1

FROM 763104351884.dkr.ecr.${AWS_REGION}.amazonaws.com/pytorch-inference:2.3-cpu-py311

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install additional dependencies from requirements.txt file
RUN pip uninstall torch torchvision -y

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -U -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

## Cleanup ##
RUN pip cache purge \
    && rm -rf /tmp/tmp* \
    && rm -iRf /root/.cache

COPY scripts/ /home/scripts/
WORKDIR /home/scripts

RUN chmod +x run_model.sh

ENV TMPDIR="/tmp"

ENTRYPOINT ["./run_model.sh"]
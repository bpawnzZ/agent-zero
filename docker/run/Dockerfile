# Use the latest slim version of Debian
FROM debian:bookworm-slim

# Check if the argument is provided, else throw an error
ARG BRANCH
RUN if [ -z "$BRANCH" ]; then echo "ERROR: BRANCH is not set!" >&2; exit 1; fi
ENV BRANCH=$BRANCH

# Copy contents of the project to /a0
COPY ./fs/ /

# Set up Docker access
RUN apt-get update && \
    apt-get install -y docker.io && \
    groupadd -g 999 docker && \
    usermod -aG docker root

# pre installation steps
RUN bash /ins/pre_install.sh $BRANCH

# install additional software
RUN bash /ins/install_additional.sh $BRANCH

# install A0
RUN bash /ins/install_A0.sh $BRANCH

# cleanup repo and install A0 without caching, this speeds up builds
ARG CACHE_DATE=none
RUN echo "cache buster $CACHE_DATE" && bash /ins/install_A02.sh $BRANCH

# post installation steps
RUN bash /ins/post_install.sh $BRANCH

# Fix permissions for Docker socket
RUN chmod 666 /var/run/docker.sock

# Expose ports
EXPOSE 22 80

# initialize runtime
CMD ["/bin/bash", "-c", "/bin/bash /exe/initialize.sh $BRANCH"]
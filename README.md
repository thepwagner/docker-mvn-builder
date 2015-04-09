# Docker Maven Builder

Experiment spawned by [dockerception](https://github.com/jamiemccrindle/dockerception).

Maven is used in the "builder" docker to grab Java code from public repos (or a private repo in S3).

The "runtime" docker uses these Maven resolved .jar files and spawns a Java process.

It builds a useless Cassandra deploy; the proof of concept is ClassLoader success.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata, copy, replace_in_file, get
import os


class MultiarenaConan(ConanFile):

    name = "multiarena"
    _version = "1.2"
    revision = ""
    version = _version+revision

    license = "Apache-2.0"
    homepage = "https://github.com/tirimatangi/MultiArena"
    url = "https://github.com/TUM-CONAN/conan-multiarena"
    description = "c++ pmr arena allocator"
    topics = ("System", "Architecture")

    settings = "os", "compiler", "build_type", "arch"
    options = {
    }
    default_options = {
    }

    def export(self):
        update_conandata(self, {"sources": {
            "commit": "main", #  "v{}".format(self.version),
            "url": "https://github.com/ulricheck/MultiArena"
            }}
            )

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=self.source_folder)
        git.checkout(commit=sources["commit"])

    def generate(self):
        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self, src_folder="source_folder")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join(self.package_folder, "include", "MultiArena-0.0.1")]
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

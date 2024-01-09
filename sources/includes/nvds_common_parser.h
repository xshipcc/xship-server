/*
 * Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

#include <vector>
#include <string>
#include <cstring>
#include <iostream>
#include <gst/gst.h>

#define _PATH_MAX 1024

/**
* Function definition to split semicolon separated string value and store tokens
* in a vector
*
* @param[in]  input A semicolon separated string.
* @return Vector containing tokens (i.e. uri(s))
*/
std::vector<std::string>
split_string (std::string input);

/**
* Function definition to get the absolute path of a file.
*
* @param[in]  cfg_file_path YAML config file name/path.
* @param[in]  file_path File name of whose absolute path is to be obtained.
* @param[in]  abs_path_str An empty char pointer. At the end of function call,
*             it contains the full path of the file.
* @return Boolean value on the basis of absolute path value.
*/
gboolean
get_absolute_file_path_yaml (
    const gchar * cfg_file_path, const gchar * file_path,
    char *abs_path_str);
/** @} */


import json
import os
from utility.filemanager import filemanager


class Build:
    """Used to generate and store different Guild Wars 2 builds"""
    # checking if the class name is valid. If not, we store it as undefined
    # -- which will not be accepted for Build functions.
    # I include shorthand version for classes as well to make it easier to use the commands
    async def new_build(self, class_name, build_name, link,):
        """This function generates a new build, adds it into the .json file.
        If it is the first build, then it creates builds.json; and enables other functions to run."""
        # load the file if it exists, or create it if it doesn't
        try:
            f = filemanager.file_open_to_read()
            data = json.load(f)
            # read from and write into the file
            for key in data.keys():
                # make sure the class and builds exist
                if class_name in data.keys() and build_name not in data[class_name]:
                    data[class_name][build_name] = link
                    response = f"{class_name} : {build_name} was successfully added."
                    break
                elif class_name in data.keys() and build_name in data[class_name]:
                    response = "This build already exists. Save it with a new name, " \
                               "or use #deletebuild or #updatebuild commands."
                # else create it, as long as the file is not empty (due to deletion of key/values)
                elif class_name not in data.keys():
                    new_data = {class_name: {build_name: link}}
                    data.update(new_data)
                    response = f"{class_name} : {build_name} was successfully added."
                    break
            # if the file exists, but it is empty
            if len(data) == 0:
                fl = filemanager.file_open_to_write()
                new_build = {class_name: {build_name: link}}
                data.update(new_build)
                fl.close()
                response = f"{class_name} : {build_name} was successfully added."
            fl = filemanager.file_open_to_write()
            json.dump(data, fl)
            fl.close()
            return response
        # if builds.json does not exist, create it.
        # though filemanager ensures this file exist at the start of the program
        # it is best to make sure nothing funny happens due to an unexpected deletion
        except FileNotFoundError:
            f = filemanager.file_open_to_write()
            new_build = {class_name: {build_name: link}}
            json.dump(new_build, f)
            f.close()
            response = f"{class_name} : {build_name} was successfully added."
            return response
        finally:
            filemanager.file_close(f)

    async def delete_build(self, class_name, build_name):
        """Deletes an existing build on builds.json. if such a build exists."""
        try:
            f = filemanager.file_open_to_read()
            data = json.load(f)
        except FileNotFoundError:
            return "There are no builds saved. Use #newbuild command first"
        try:
            for key, value in data.items():
                # logic whether the given class or build name exists or not
                if class_name != key or build_name not in value:
                    response = "Could not find the class/build combination"
                # if the class & build exist within builds.json, delete it
                elif class_name == key and build_name in value:
                    del value[build_name]
                    # remove the class object too, if it has no more builds(key pair values)
                    if len(data[class_name]) == 0:
                        data2 = data.copy()
                        del data2[class_name]
                        data = data2
                    response = f"{build_name} was removed"
                    break
            fl = filemanager.file_open_to_write()
            json.dump(data, fl)
            fl.close()
            return response
        finally:
            filemanager.file_close(f)

    async def update_build(self, class_name, build_name, link):
        """Updates existing builds that are in builds.json. if such a build exists."""
        try:
            f = filemanager.file_open_to_read()
            data = json.load(f)
        except FileNotFoundError:
            return "There are no builds saved. Use #newbuild command first"
        try:
            for key, value in data.items():
                # make sure the class and builds exist
                if class_name not in key:
                    response = f"No classes found for '{class_name}'. #build for available classes information."

                elif class_name == key and build_name not in value:
                    response = f"No such build was found for {class_name}"

                # only get the correct class and build name combination
                elif class_name == key and build_name in value:
                    value[build_name] = value[build_name].replace(value[build_name], link)
                    response = f"{build_name} was successfully updated."
                    break
            fl = filemanager.file_open_to_write()
            json.dump(data, fl)
            fl.close()
            return response

        finally:
            filemanager.file_close(f)

    async def show_build(self, name):
        """Reads from builds.json to show the key-pair values,
         if any exists, for the given class. Else, nothing is returned"""
        try:
            f = filemanager.file_open_to_read()
            data = json.load(f)
        except FileNotFoundError:
            return "There are no builds saved. Use #newbuild command first"
        try:
            for class_name, builds in data.items():
                if class_name == name:
                    return f"{class_name}".title()+f" builds: {builds}"
            return f"There is no such build/class. Check #build to see the list of builds."
        finally:
            filemanager.file_close(f)


    async def currently_available_builds(self):
        """a quick reminder to let users know what commands they can use based on the available builds"""
        try:
            f = filemanager.file_open_to_read()
            data = json.load(f)
        except FileNotFoundError:
            return "No builds saved"
        try:
            classes = []
            for key, value in data.items():
                classes.append(key)
            if len(classes) == 0:
                response = "There are currently no builds saved"
            else:
                response = f"Current classes with builds: {classes}." \
                            f" Use #builds and type any of these names to see builds. => #builds elementalist"
            return response
        finally:
            filemanager.file_close(f)

build = Build()



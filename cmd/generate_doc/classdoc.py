import argparse
import os.path
import subprocess
import sys
from collections import OrderedDict
import re
import scene_rdl2
from jinja2 import Environment, FileSystemLoader
from math import log10, floor

hex_re              = re.compile('0[xX][0-9a-fA-F]+')

def replace_mem_address(input):
    return hex_re.sub('...', str(input))

def interfaceSet(interface):
    """ converts a SceneObjectInterface bit set into
        a Python set of string names"""
    s = set()
    bits = int(interface)
    for (v,i) in scene_rdl2.SceneObjectInterface.values.items():
        if i == scene_rdl2.SceneObjectInterface.GENERIC: continue
        if bits & v: s.add(i.name)
    return s

class ScnClass(object):
    """ represents a SceneClass in the data passed to the template
        a sample object is used to get the attribute default values"""
    def __init__(self,rdlCls,rdlObj):
        self.rdlCls = rdlCls
        self.name = rdlCls.getName()
        self.interfaces = interfaceSet(rdlCls.getDeclaredInterface())
        self.attributes = []
        attrMap = {}
        # generate flat list of attributes under .attributes
        for name in sorted(rdlCls.getAttributeNames()):
            a = Attr(rdlCls.getAttribute(name),
                     rdlObj.get(name))
            self.attributes.append(a)
            attrMap[name] = a
        # generate grouped attributes under .groups
        self.groups = []
        for group in sorted(rdlCls.getAttributeGroupNames()):
            names = []
            for i in range(rdlCls.getAttributeGroupSize(group)):
                names.append(rdlCls.getAttributeFromGroup(group,i).getName())
            attrs = []
            for name in sorted(names):
                attrs.append(attrMap[name])
                del attrMap[name]
            self.groups.append(AttrGroup(group,attrs))
        if len(attrMap) > 0:
            attrs = []
            for name in sorted(attrMap.keys()):
                attrs.append(attrMap[name])
            self.groups.append(AttrGroup("General",attrs))

    def get_site_paths(self):
        """ determine site organization based on SceneClass"""

        # Unfortunately we cannot currently rely on the class's .interfaces
        # set because many are incomplete or empty altogether, so for now we'll
        # use regular expression matching based on the class name
        for pattern, paths in self.site_paths.items():
            if (pattern.match(self.name)):
                return paths

        return []

    # defines a set of rules on how to organize the SceneClasses on the documentation site.
    # Note that these Rules are not mutually exclusive, thus they are ordered
    site_paths = OrderedDict([
        (re.compile(".*Camera(_v[0-9]*)?$")              , ["user-reference/scene-objects", "cameras"]),
        (re.compile(".*Displacement(_v[0-9]*)?$")        , ["user-reference/scene-objects", "displacement"]),
        (re.compile(".*DisplayFilter(_v[0-9]*)?$")       , ["user-reference/scene-objects", "display-filters"]),
        (re.compile(".*Geometry(_v[0-9]*)?$")            , ["user-reference/scene-objects", "geometry"]),
        (re.compile("^GeometrySet$")                     , ["user-reference/scene-objects", "geometry-set"]),
        (re.compile(".*Joint$")                          , ["user-reference/scene-objects", "joint"]),
        (re.compile(".*Layer$")                          , ["user-reference/scene-objects", "layer"]),
        (re.compile(".*Light(_v[0-9]*)?$")               , ["user-reference/scene-objects", "lights"]),
        (re.compile(".*LightFilter(_v[0-9]*)?$")         , ["user-reference/scene-objects", "light-filters"]),
        (re.compile("^LightFilterSet$")                  , ["user-reference/scene-objects", "light-filter-set"]),
        (re.compile("^LightSet$")                        , ["user-reference/scene-objects", "light-set"]),
        (re.compile(".*NormalMap(_v[0-9]*)?$")           , ["user-reference/scene-objects", "normal-maps"]),
        (re.compile("^(?!.*(Normal)).*Map(_v[0-9]*)?$")  , ["user-reference/scene-objects", "maps"]),
        (re.compile("^Dwa.*Material(_v[0-9]*)?$")        , ["user-reference/scene-objects", "materials", "dwa"]),
        (re.compile("^Hair.*Material(_v[0-9]*)?$")       , ["user-reference/scene-objects", "materials", "hair"]),
        (re.compile(".*Material(_v[0-9]*)?$")            , ["user-reference/scene-objects", "materials"]),
        (re.compile("^Metadata$")                        , ["user-reference/scene-objects", "meta-data"]),
        (re.compile("^RenderOutput$")                    , ["user-reference/scene-objects", "render-output"]),
        (re.compile("^SceneVariables$")                  , ["user-reference/scene-objects", "scene-variables"]),
        (re.compile("^ShadowReceiverSet$")               , ["user-reference/scene-objects", "shadow-receiver-set"]),
        (re.compile("^ShadowSet$")                       , ["user-reference/scene-objects", "shadow-set"]),
        (re.compile("^TraceSet$")                        , ["user-reference/scene-objects", "trace-set"]),
        (re.compile("^UserData$")                        , ["user-reference/scene-objects", "user-data"]),
        (re.compile(".*Volume(_v[0-9]*)?$")              , ["user-reference/scene-objects", "volumes"]),
        (re.compile("^UsdPreviewSurface$")               , ["user-reference/scene-objects", "materials"]),
        (re.compile("^Usd.*")                            , ["user-reference/scene-objects", "maps"]),
        (re.compile("^NormalToRgbMap$")                  , ["user-reference/scene-objects", "maps"])
    ])

class AttrGroup(object):
    """ represents a group of attributes
         in the data passed to the template"""
    def __init__(self,name,attrs):
        self.name = name
        self.attributes = attrs

def objTypeStr(rdlAttr):
    """ the type name to use when getTypeName() returns 'SceneObject'"""
    ot = str(rdlAttr.getObjectTypeStr())
    if ot == 'Generic': ot = 'Object'
    return ot

class Attr(object):
    """ represents an attribute in the data passed to the template"""
    def __init__(self,rdlAttr,defaultValue):
        self.rdlAttr = rdlAttr
        self.defaultValue = defaultValue

    @property
    def name(self): return self.rdlAttr.getName()
    @property
    def default_value(self):
        # round floats to 6 significant digits
        if self.rdlAttr.getTypeName() == "Float":
            if (self.defaultValue == 0):
                return self.defaultValue
            return round(self.defaultValue, -int(floor(log10(abs(self.defaultValue)))) + 5)
        return self.defaultValue
    @property
    def type(self): 
        t = self.rdlAttr.getTypeName()
        if t == 'SceneObject': return objTypeStr(self.rdlAttr)
        elif t == 'SceneObjectVector': return objTypeStr(self.rdlAttr) + " Vector"
        return t
    @property
    def bindable(self): return self.rdlAttr.isBindable()
    @property
    def blurrable(self): return self.rdlAttr.isBlurrable()
    @property
    def enum(self): return self.rdlAttr.isEnumerable()
    @property
    def file(self): return self.rdlAttr.isFilename()
    @property
    def hasComment(self): return 'comment' in self.rdlAttr.getMetaDataKeys()
    @property
    def comment(self): 
        return self.rdlAttr.getMetadata('comment')
    @property
    def flags(self):
        """ flags as a list of strings"""
        f = []
        if self.bindable: f.append('bindable')
        if self.blurrable: f.append('blurrable')
        if self.enum: f.append('enum')
        if self.file: f.append('filename')
        return f
    @property
    def hasFlags(self):
        return len(self.flags) > 0
    @property
    def enumValues(self):
        """ returns (name,val) pairs for attr's enum values """
        v = []
        for k in self.rdlAttr.getEnumValKeys():
            v.append((self.rdlAttr.getEnumDescription(k),k))
        return v

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Moonray class documentation from templates")

    parser.add_argument('-c','--class',
                        dest='class_name',
                        help='Class to generate')
    parser.add_argument('-i','--interface',
                       help='Generate all classes with the given interface. NOTE: This is unreliable due to incomplete class definitions')
    parser.add_argument('-t','--template',
                        default='default_template.md',
                        help='Specify template file to use')
    parser.add_argument('-d','--dir',
                        help='Specify output directory. This should likely be the "docs" folder in your documentation repo')
    parser.add_argument('-a','--all', action='store_true',
                        help='Generate all classes')
    parser.add_argument('--images', action='store_true',
                        help='Also render documentation images with generate_doc_images: with -a, for '
                             'every class with a manifest.json; with -c, the class must have one')

    args = parser.parse_args()
    if args.images and args.interface:
        parser.error('--images can\'t be used with -i; use -a or -c')
    return args

def render_images(args):
    """ runs generate_doc_images for the same classes and docs folder"""
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'generate_doc_images', 'generate_doc_images.py')
    cmd = [sys.executable, script]
    cmd += ['-a'] if args.all else ['-c', args.class_name]
    if args.dir:
        cmd += ['-d', args.dir]
    sys.stdout.flush()
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def generate(cls,template,dir=None):
    if dir is not None:
        output = dir

    paths = cls.get_site_paths()
    if not paths:
        print("Warning: no rule found for organizing {}, skipping\n".format(cls.name))
        return

    liquid_paths = [paths[0], paths[1]]
    liquid_paths[0] = liquid_paths[0].replace("/", ".")
    data_path = 'site.data.{}.{}'.format('.'.join(liquid_paths), cls.name)
    subdirs = os.path.join('', *paths)
    output = os.path.join(output, subdirs)
    if output and not os.path.isdir(output):
        os.makedirs(output)

    result = template.render({
        'class'     : cls,
        'data_path' : data_path,
    })

    filename = cls.name + ".md"
    output = os.path.join(output, filename)

    with open(output,'w') as f:
        f.write(result)
    print("Wrote {}".format(output))

def main():
    env = Environment(loader=FileSystemLoader("."))
    env.filters['replace_mem_address'] = replace_mem_address
    args = parse_args()
    template = env.get_template(args.template)
    context = scene_rdl2.SceneContext()
    context.setProxyModeEnabled(True)

    if args.dir and not os.path.isdir(args.dir):
        os.makedirs(args.dir)

    if args.all:
        context.loadAllSceneClasses()
        for clsname in context.getSceneClassNames():
            if clsname.startswith("Test"):
                continue
            cls = context.getSceneClass(clsname)
            obj = context.createSceneObject(clsname,clsname+"_obj")
            scncls = ScnClass(cls,obj)
            generate(scncls,template,args.dir)

    elif args.interface:
        try:
            interface = getattr(scene_rdl2.SceneObjectInterface,
                                args.interface.upper())
        except AttributeError:
            print("Unknown interface: "+args.interface)
            return
        context.loadAllSceneClasses()
        for clsname in context.getSceneClassNames():
            if clsname.startswith("Test"):
                continue
            cls = context.getSceneClass(clsname)
            bits = int(cls.getDeclaredInterface())
            if bits & int(interface): 
                obj = context.createSceneObject(clsname,clsname+"_obj")
                generate(ScnClass(cls,obj),template,args.dir)
    elif args.class_name:
        if args.class_name.startswith("Test"):
            print("Skipping test class: "+args.class_name)
            return
        cls = context.createSceneClass(args.class_name)
        obj = context.createSceneObject(args.class_name,args.class_name+"_obj")
        generate(ScnClass(cls,obj),template,args.dir)
    else:
        print("Specify a class name, an interface, or --all.")
        return

    if args.images:
        render_images(args)

main()

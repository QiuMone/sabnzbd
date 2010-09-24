#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
# Copyright 2010 The SABnzbd-Team <team@sabnzbd.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Compile PO files to MO files

import glob
import os
import re
import sys
import gettext

PO_DIR = 'po/main'
POE_DIR = 'po/email'
PON_DIR = 'po/nsis'
MO_DIR = 'locale'
EMAIL_DIR = 'email'

MO_LOCALE = '/LC_MESSAGES'
DOMAIN = 'SABnzbd'
DOMAIN_E = 'SABemail'
DOMAIN_N = 'SABnsis'
LANG_MARKER = 'language.txt'
NSIS= 'NSIS_Installer.nsi'

LanguageTable = {
    'aa' : ('Afar', 'Afaraf'),
    'af' : ('Afrikaans', 'Afrikaans'),
    'ak' : ('Akan', 'Akan'),
    'sq' : ('Albanian', 'Shqip'),
    'an' : ('Aragonese', 'Aragonés'),
    'ae' : ('Avestan', 'Avesta'),
    'ay' : ('Aymara', 'Aymararu'),
    'bm' : ('Bambara', 'Bamanankan'),
    'eu' : ('Basque', 'Euskara'),
    'bi' : ('Bislama', 'Bislama'),
    'bs' : ('Bosnian', 'Bosanskijezik'),
    'br' : ('Breton', 'Brezhoneg'),
    'ca' : ('Catalan', 'Català'),
    'ch' : ('Chamorro', 'Chamoru'),
    'kw' : ('Cornish', 'Kernewek'),
    'co' : ('Corsican', 'Corsu'),
    'hr' : ('Croatian', 'Hrvatski'),
    'cs' : ('Czech', 'Cesky, ceština'),
    'da' : ('Danish', 'Dansk'),
    'nl' : ('Dutch', 'Nederlands'),
    'en' : ('English', 'English'),
    'eo' : ('Esperanto', 'Esperanto'),
    'et' : ('Estonian', 'Eesti'),
    'fo' : ('Faroese', 'Føroyskt'),
    'fj' : ('Fijian', 'Vosa Vakaviti'),
    'fi' : ('Finnish', 'Suomi'),
    'fr' : ('French', 'Français'),
    'gl' : ('Galician', 'Galego'),
    'de' : ('German', 'Deutsch'),
    'hz' : ('Herero', 'Otjiherero'),
    'ho' : ('Hiri Motu', 'Hiri Motu'),
    'hu' : ('Hungarian', 'Magyar'),
    'id' : ('Indonesian', 'Bahasa Indonesia'),
    'ga' : ('Irish', 'Gaeilge'),
    'io' : ('Ido', 'Ido'),
    'is' : ('Icelandic', 'Íslenska'),
    'it' : ('Italian', 'Italiano'),
    'jv' : ('Javanese', 'BasaJawa'),
    'rw' : ('Kinyarwanda', 'Ikinyarwanda'),
    'kg' : ('Kongo', 'KiKongo'),
    'kj' : ('Kwanyama', 'Kuanyama'),
    'la' : ('Latin', 'Lingua latina'),
    'lb' : ('Luxembourgish', 'Lëtzebuergesch'),
    'lg' : ('Luganda', 'Luganda'),
    'li' : ('Limburgish', 'Limburgs'),
    'ln' : ('Lingala', 'Lingála'),
    'lt' : ('Lithuanian', 'Lietuviukalba'),
    'lv' : ('Latvian', 'Latviešuvaloda'),
    'gv' : ('Manx', 'Gaelg'),
    'mg' : ('Malagasy', 'Malagasy fiteny'),
    'mt' : ('Maltese', 'Malti'),
    'nb' : ('Norwegian Bokmål', 'Norsk bokmål'),
    'nn' : ('Norwegian Nynorsk', 'Norsk nynorsk'),
    'no' : ('Norwegian', 'Norsk'),
    'oc' : ('Occitan', 'Occitan'),
    'om' : ('Oromo', 'Afaan Oromoo'),
    'pl' : ('Polish', 'Polski'),
    'pt' : ('Portuguese', 'Português'),
    'rm' : ('Romansh', 'Rumantsch grischun'),
    'rn' : ('Kirundi', 'kiRundi'),
    'ro' : ('Romanian', 'Româna'),
    'sc' : ('Sardinian', 'Sardu'),
    'se' : ('Northern Sami', 'Davvisámegiella'),
    'sm' : ('Samoan', 'Gagana fa\'a Samoa'),
    'gd' : ('Gaelic', 'Gàidhlig'),
    'sn' : ('Shona', 'Chi Shona'),
    'sk' : ('Slovak', 'Slovencina'),
    'sl' : ('Slovene', 'Slovenšcina'),
    'st' : ('Southern Sotho', 'Sesotho'),
    'es' : ('Spanish Castilian', 'Español, castellano'),
    'su' : ('Sundanese', 'Basa Sunda'),
    'sw' : ('Swahili', 'Kiswahili'),
    'ss' : ('Swati', 'SiSwati'),
    'sv' : ('Swedish', 'Svenska'),
    'tn' : ('Tswana', 'Setswana'),
    'to' : ('Tonga (Tonga Islands)', 'faka Tonga'),
    'tr' : ('Turkish', 'Türkçe'),
    'ts' : ('Tsonga', 'Xitsonga'),
    'tw' : ('Twi', 'Twi'),
    'ty' : ('Tahitian', 'Reo Tahiti'),
    'wa' : ('Walloon', 'Walon'),
    'cy' : ('Welsh', 'Cymraeg'),
    'wo' : ('Wolof', 'Wollof'),
    'fy' : ('Western Frisian', 'Frysk'),
    'xh' : ('Xhosa', 'isi Xhosa'),
    'yo' : ('Yoruba', 'Yorùbá'),
    'zu' : ('Zulu', 'isi Zulu'),
}

# Determine location of PyGetText tool
path, exe = os.path.split(sys.executable)
if os.name == 'nt':
    TOOL = os.path.join(path, r'Tools\i18n\msgfmt.py')
else:
    TOOL = os.path.join(path, 'msgfmt.py')
if not os.path.exists(TOOL):
    TOOL = 'msgfmt'


# Filter for retrieving readable language from PO file
RE_LANG = re.compile(r'"Language-Description:\s([^"]+)\\n')

def process_po_folder(domain, folder):
    """ Process each PO file in folder
    """
    for fname in glob.glob(os.path.join(folder, '*.po')):
        podir, basename = os.path.split(fname)
        name, ext = os.path.splitext(basename)
        mo_path = os.path.normpath('%s/%s%s' % (MO_DIR, name, MO_LOCALE))
        mo_name = '%s.mo' % domain
        if not os.path.exists(mo_path):
            os.makedirs(mo_path)

        # Create the MO file
        mo_file = os.path.join(mo_path, mo_name)
        print 'Compile %s' % mo_file
        ret = os.system('%s -o %s %s' % (TOOL, mo_file, fname))
        if ret != 0:
            print '\nMissing %s. Please install this package first.' % TOOL
            exit(1)

def remove_mo_files():
    """ Remove MO files in locale
    """
    for root, dirs, files in os.walk(MO_DIR, topdown=False):
        for f in files:
            if not f.startswith(DOMAIN):
                os.remove(os.path.join(root, f))


def make_templates():
    """ Create email templates
    """
    if not os.path.exists('email'):
        os.makedirs('email')
    for path in glob.glob(os.path.join(MO_DIR, '*')):
        lng = os.path.split(path)[1]
        print 'Create email template for %s' % lng
        trans = gettext.translation(DOMAIN_E, MO_DIR, [lng], fallback=False, codeset='latin-1')
        # The unicode flag will make _() return Unicode
        trans.install(unicode=True, names=['lgettext'])

        src = open(EMAIL_DIR + '/email-en.tmpl', 'r')
        data = src.read().decode('utf-8')
        src.close()
        data = _(data).encode('utf-8')
        fp = open('email/email-%s.tmpl' % lng, 'wb')
        fp.write(data)
        fp.close()

        src = open(EMAIL_DIR + '/rss-en.tmpl', 'r')
        data = src.read().decode('utf-8')
        src.close()
        data = _(data).encode('utf-8')
        fp = open('email/rss-%s.tmpl' % lng, 'wb')
        fp.write(data)
        fp.close()
        mo_path = os.path.normpath('%s/%s%s/%s.mo' % (MO_DIR, path, MO_LOCALE, DOMAIN_E))
        if os.path.exists(mo_path):
            os.remove(mo_path)


def patch_nsis():
    """ Patch translation into the NSIS script
    """
    RE_NSIS = re.compile(r'^(\s*LangString\s+\w+\s+\$\{LANG_)(\w+)\}\s+(".*)', re.I)
    languages = [os.path.split(path)[1] for path in glob.glob(os.path.join(MO_DIR, '*'))]

    src = open(NSIS, 'r')
    new = []
    for line in src:
        m = RE_NSIS.search(line)
        if m:
            leader = m.group(1)
            langname = m.group(2).upper()
            text = m.group(3).strip('"\n')
            if langname == 'ENGLISH':
                # Write back old content
                new.append(line)
                # Replace silly $\ construction with just a \
                text = text.replace('$\\"', '"').replace('$\\', '\\')
                for lcode in languages:
                    lng = LanguageTable.get(lcode)
                    if lng and lcode != 'en':
                        lng = lng[0].upper()
                        trans = gettext.translation(DOMAIN_N, MO_DIR, [lcode], fallback=False, codeset='latin-1')
                        # The unicode flag will make _() return Unicode
                        trans.install(unicode=True, names=['lgettext'])
                        trans = lgettext(text)
                        trans = trans.replace('\\', '$\\').replace('"', '$\\"')
                        line = '%s%s} "%s"\n' % (leader, lng, trans)
                        new.append(line)
                    elif lng is None:
                        print 'Warning: unsupported language %s, add to table in this script' % langname
        else:
            new.append(line)
    src.close()

    dst = open(NSIS, 'w')
    for line in new:
        dst.write(line)
    dst.close()


if len(sys.argv) > 1 and sys.argv[1] == 'all':
    print 'Email MO files'
    process_po_folder(DOMAIN_E, POE_DIR)

    print 'NSIS MO file'
    process_po_folder(DOMAIN_N, PON_DIR)

    print "Create email templates from MO files"
    make_templates()

    print "Patch NSIS script"
    patch_nsis()

print 'Main program MO files'
process_po_folder(DOMAIN, PO_DIR)

print "Remove temporary templates"
remove_mo_files()

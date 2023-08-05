/*
 * @file    rsc68.c
 * @brief   resource functions
 * @author  http://sourceforge.net/users/benjihan
 *
 * Copyright (C) 1998-2011 Benjamin Gerard
 *
 * Time-stamp: <2011-10-12 13:22:58 ben>
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.
 *
 * If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifdef HAVE_CONFIG_H
# include "config.h"
#endif
#include "file68_api.h"
#include "rsc68.h"

#include "error68.h"
#include "url68.h"
#include "string68.h"
#include "alloc68.h"
#include "istream68_file.h"
#include "istream68_fd.h"
#include "istream68_curl.h"
#include "msg68.h"

#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


#ifndef DEBUG_RSC68_O
#define DEBUG_RSC68_O 0
#endif
int rsc68_cat = msg68_DEFAULT;

static volatile int init = 0;

/* The resource pathes are context independant consequently
 * each context use the same pathes.
 */
static const char * share_path  = 0; /* Shared resource path. */
static const char * user_path   = 0; /* User resource path.   */
static const char * lmusic_path = 0; /* Local music path.     */
static const char * rmusic_path = 0; /* Remote music path.    */

static istream68_t * default_open(rsc68_t type, const char *name, int mode,
                                  rsc68_info_t * info);

static rsc68_handler_t rsc68 = default_open;

#ifndef FILE68_SHARED_PATH
# define FILE68_SHARED_PATH 0
#endif
#ifndef PACKAGE_URL
# define FILE68_RMUSIC_PATH 0
#else
# define FILE68_RMUSIC_PATH PACKAGE_URL "/Download/Music"
#endif
#ifndef FILE68_USER_PATH
# define FILE68_USER_PATH 0
#endif
#ifndef FILE68_MUSIC_PATH
# define FILE68_MUSIC_PATH 0
#endif

static struct {
  rsc68_t type;
  const char * name;
  const char * path;
  const char * ext;
} rsc68_table[rsc68_last];

static void rsc68_init_table(void)
{
  memset(rsc68_table, 0, sizeof(rsc68_table));

  rsc68_table[rsc68_replay].type = rsc68_replay;
  rsc68_table[rsc68_replay].name = "replay";
  rsc68_table[rsc68_replay].path = "/Replay/";
  rsc68_table[rsc68_replay].ext  = ".bin";

  rsc68_table[rsc68_config].type = rsc68_config;
  rsc68_table[rsc68_config].name = "config";
  rsc68_table[rsc68_config].path = "/";
  rsc68_table[rsc68_config].ext  = ".cfg";

  rsc68_table[rsc68_sample].type = rsc68_sample;
  rsc68_table[rsc68_sample].name = "sample";
  rsc68_table[rsc68_sample].path = "/Sample/";
  rsc68_table[rsc68_sample].ext  = ".sc68";


  rsc68_table[rsc68_dll].type = rsc68_dll;
  rsc68_table[rsc68_dll].name = "dll";
  rsc68_table[rsc68_dll].path = "/Dll/";
  rsc68_table[rsc68_dll].ext  = 0;

  rsc68_table[rsc68_music].type = rsc68_music;
  rsc68_table[rsc68_music].name = "music";
  rsc68_table[rsc68_music].path = "/Music/";
  rsc68_table[rsc68_music].ext  = ".sc68";
}

static const char *default_share_path(void)
{
  return share_path
    ? share_path
    : FILE68_SHARED_PATH;
}

static const char *default_rmusic_path(void)
{
  return rmusic_path
    ? rmusic_path
    : FILE68_RMUSIC_PATH;
}

static const char * rsc_set_any(const char ** any, const char * path)
{
  free68((void *)*any);
  return *any = strdup68(path) ;
}

const char * rsc68_set_share(const char *path)
{
  return rsc_set_any(&share_path, path);
}

const char * rsc68_set_user(const char *path)
{
  return rsc_set_any(&user_path, path);
}

const char * rsc68_set_music(const char *path)
{
  return rsc_set_any(&lmusic_path, path);
}

const char * rsc68_set_remote_music(const char *path)
{
  return rsc_set_any(&rmusic_path, path);
}

void rsc68_get_path(const char **share,
                    const char **user,
                    const char **local_music,
                    const char **remote_music)
{
  if (share)        *share        = share_path;
  if (user)         *user         = user_path;
  if (local_music)  *local_music  = lmusic_path;
  if (remote_music) *remote_music = rmusic_path;
}

/* Returns char or -1 to skip it */
typedef int (*char_cv_t)(int);

/* Runs the convert chain */
static int convert_chain(int c, ...)
{
  va_list list;
  char_cv_t cv;

  va_start(list,c);
  while (cv = va_arg(list,char_cv_t), cv) {
    c = cv(c);
  }
  va_end(list);
  return c;
}

/* No conversion */
#if 0
static int cv_none(int c) {
  return c;
}
#endif

/* Convert upper to lower */
static int cv_lower(int c) {
  return (c>='A' && c <= 'Z')
    ? c - 'A' + 'a'
    : c;
}

static int cv_from_tables(int c, const char * acc, const char * con)
{
  const char * s;
  if (s=strchr(acc,c), s) {
    c = con[s-acc];
  }
  return c;
}

/* Convert accented */
/* $$$ TODO ... Proper encoding */
static int cv_accent(int c)
{
  return cv_from_tables(c,
                        "áâàãäëéêèïíîìöõóôòüúûùüç",
                        "aaaaaeeeeiiiiooooouuuuuc");
}

/* Convert to minus */
static int cv_minus(int c)
{
  if (strchr("\\/&$",c)) c = '-';
  return c;
}

/* Convert to "skip" */
#if 0
static int cv_skip(int c)
{
  if (strchr(":?<>",c)) c = -1;
  return c;
}
#endif

/* Convert to "skip" */
static int cv_skip2(int c)
{
  if (strchr("<>",c)) c = -1;
  return c;
}

/* Convert for filename in local filesystem */
static int cv_name_local(int c)
{
  c = cv_accent(cv_minus(cv_skip2(c)));
  return c;
}

static int cv_path_local(int c)
{
  if (c == '\\') c = '/';
  if (c != '/') {
    c = cv_name_local(c);
  }
  return c;
}

static int cv_name_remote(int c)
{
  c = cv_accent(cv_minus(cv_skip2(c)));
  if (c == ' ') c = '_';
  else if (c == '#') c = '0';
  return c;
}

static int cv_path_remote(int c)
{
  if (c == '\\') c = '/';
  if (c != '/') {
    c = cv_name_remote(c);
  }
  return c;
}


static int copy_path(char *d, int max,
                     const char * s,
                     char_cv_t cv1,
                     char_cv_t cv2,
                     int brk)
{
  int i;

  for (i=0; i<max; ) {
    int c = (*s++) & 255, c2;
    if (!c) break;
    c2 = convert_chain(c, cv1, cv2, 0);
    if (c2 != -1) {
      d[i++] = c2;
    }
    if (c == brk) break;
  }
  if (i < max) {
    d[i] = 0;
  } else {
    i = -1;
  }
  return i;
}

/* formay is /:track:loop:time/ */
const char * rsc68_get_music_params(rsc68_info_t *info, const char *name)
{
  int c = 1;                    /* anything but 0 or ':' */
  if (info) {
    info->type = rsc68_last;
  }

  if (name) c = *name;
  if (!c || c == ':') {
    int i, tinfo[3] = { -1, -1, -1 };

    for (i=0; i<3 && c == ':'; ++i) {
      c = *++name;
      if (c >= '0' && c <= '9') {
        int v = 0;
        do {
          v = v*10 + c-'0';
          c = *++name;
        } while (c >= '0' && c <= '9');
        tinfo[i] = v;
      }
    }
    /* skip to eos or next '/' */
    while (c && c != '/') {
      c = *++name;
    }

    if (info) {
      info->type = rsc68_music;
      info->data.music.track = tinfo[0];
      info->data.music.loop  = tinfo[1];
      info->data.music.time  = tinfo[2];
    }
  }

  return name;
}



/* author/hw/title[/:track:loop:time] */
static char * convert_music_path(char * newname, int max,
                                 const char *name,
                                 rsc68_info_t * info)
{
  int len, c;
  char * nname = newname;
  char * ename = nname+max;

  /* Author */
  len = copy_path(nname, ename - nname, name, 0, 0, '/');
  if (len <= 0) goto error;
  nname += len;
  name  += len;

  /* Hardware */
  c = (*name++) & 255;

  if (c == '0') {
    len = copy_path(nname, ename - nname, "Atari ST/", 0, 0, 0);
  } else if (c == '1') {
    len = copy_path(nname, ename - nname, "Amiga/", 0, 0, 0);
  } else {
    len = -1;
  }
  if (len <= 0) goto error;
  nname += len;
  c = (*name++) & 255;
  if (c != '/') goto error;

  /* Title */
  len = copy_path(nname, ename - nname, name, 0, 0, '/');
  if (len <= 0) goto error;
  nname += len;
  name  += len;

  if (nname[-1] == '/') {
    --nname;
  }
  *nname = 0;

  /* Optional track # */
  name = rsc68_get_music_params(info, name);

  return newname;

error:
  *newname = 0;
  return 0;
}

static istream68_t * default_open(rsc68_t type, const char *name,
                                  int mode, rsc68_info_t * info)
{
  istream68_t * is = 0;
  int err = -1;
  const char *subdir = 0, *ext = 0;
  char tmp[1024], * apath = 0;
  char tmpname[512];
  int alen = 0;

  char_cv_t cv_path=0, cv_extra=0;

  struct {
    const char * path, * sdir, * ext;
    int curl;
  } pathes[4];
  int ipath, npath = 0;
  const char * share_path  = default_share_path();
  const char * rmusic_path = default_rmusic_path();

  /* default to invalid type. */
  if (info) {
    info->type = rsc68_last;
  }

  if ( (int) type < 0 || (int)type >= rsc68_last) {
    return 0;
  }

  memset(pathes,0,sizeof(pathes));

  if (type == rsc68_music && lmusic_path) {
    /* local music path is prior to user share */
    pathes[npath].path = lmusic_path;
    pathes[npath].sdir = "/";
    ++npath;
  }

  /* Build default pathes list */
  if (user_path) {
    pathes[npath++].path = user_path;
  }

  if (mode == 1 && share_path) {
    pathes[npath++].path = share_path;
  }

  subdir = rsc68_table[type].path;
  ext    = rsc68_table[type].ext;

  /* Set a default name for config file if none is given. */
  if (type == rsc68_config && (!name || !name[0])) {
    name = "sc68";
  }

  TRACE68(rsc68_cat,"rsc68: open %c 'rsc68://%s/%s%s'\n",
          (mode==1)?'R':'W',rsc68_table[type].name, name, ext?ext:"");

  /* Any specific stuff. */
  switch (type) {
  case rsc68_replay:
    cv_extra = cv_lower; /* $$$ transform replay name to lower case. */
    break;

  case rsc68_music:
    if (mode == 1 && rmusic_path) {
      pathes[npath].path = rmusic_path;
      pathes[npath].sdir = "/";
      pathes[npath].curl = 1;
      ++npath;
    }
    name = convert_music_path(tmpname, sizeof(tmpname), name, info);
    break;

  default:
    break;
  }

  for (ipath=0; name && ipath < npath; ++ipath) {
    const char *cpath, * cdir, * cext;
    char *p, *pe, *path;
    int len, l;

    cpath = pathes[ipath].path;
    cdir  = pathes[ipath].sdir ? pathes[ipath].sdir : subdir;
    cext  = pathes[ipath].ext ? pathes[ipath].ext : ext;

    len = 1
      + strlen(cpath)
      + strlen(cdir)
      + strlen(name)
      + (cext ? strlen(cext) : 0);

    if (len <= alen) {
      path = apath;
    } else if (len  <= sizeof(tmp)) {
      path = tmp;
    } else {
      free68(apath);
      apath = alloc68(len);
      alen = apath ? len : 0;
      path = apath;
    }

    if (!path) {
      continue;
    }

    p = path;
    pe = path + len;

    cv_path = pathes[ipath].curl
      ? cv_path_remote
      : cv_path_local;

    /* Build path. */
    l = copy_path(p, pe-p, cpath, cv_path, 0 , 0);
    p += l;
    l = copy_path(p, pe-p, cdir, cv_path, 0, 0);
    p += l;
    l = copy_path(p, pe-p, name, cv_path, cv_extra, 0);
    p += l;
    if (cext) {
      l = copy_path(p, pe-p, cext, 0, 0 ,0);
      p += l;
    }

    if (pathes[ipath].curl) {
      TRACE68(rsc68_cat,"rsc68: try open '%s' with curl\n", path);
      is = istream68_curl_create(path, mode);
    } else {
      TRACE68(rsc68_cat,"rsc68: try open '%s' with file\n", path);
      is = istream68_file_create(path, mode);
      if (!is) {
        TRACE68(rsc68_cat,"rsc68: try open '%s' with FD\n", path);
        is = istream68_fd_create(path, -1, mode);
      }
    }
    err = istream68_open(is);
    TRACE68(rsc68_cat, "rsc68: try [%s]\n", strok68(err));
    if (!err) {
      break;
    }

    istream68_destroy(is);
    is = 0;
  }

  if (apath != tmp) {
    free68(apath);
  }
  if (err) {
    istream68_destroy(is);
    is = 0;
  }

  if (is && info) {
    info->type = type;
  }

  TRACE68(rsc68_cat, "rsc68: open '%s' => [%s,%s]\n",
          strok68(!is), istream68_filename(is));
  return is;
}


rsc68_handler_t rsc68_set_handler(rsc68_handler_t fct)
{
  rsc68_handler_t old;

  old = rsc68;
  if (fct) {
    rsc68 = fct;
  }
  return old;
}

istream68_t * rsc68_create_url(const char *url, int mode, rsc68_info_t * info)
{
  istream68_t * is;

  /* $$$ Ugly haXXX we need to close since created stream are not
     supposed to be open but that's the only function we have
     for now. */
  is = rsc68_open_url(url, mode, info);
  istream68_close(is);
  return is;
}


istream68_t * rsc68_open_url(const char *url, int mode, rsc68_info_t * info)
{
  int i;
  char protocol[16];
  istream68_t * is = 0;

  TRACE68(rsc68_cat,"rsc68: open url='%s' mode=%c%c%s)\n",
          strnevernull68(url),
          (mode&1) ? 'R' : '.',
          (mode&2) ? 'W' : '.',
          info ? " with info" : "");

  if (info) {
    info->type = rsc68_last;
  }
  if (!rsc68) {
    msg68_critical("rsc68: no handler defined\n");
    goto error;
  }
  if (mode < 1 || mode > 2) {
    msg68_critical("rsc68: invalid open mode %d\n",mode);
    goto error;
  }

  if (url68_get_protocol(protocol, sizeof(protocol), url) ||
      strcmp68(protocol,"RSC68")) {
    msg68_error("rsc68: missing or invalid protocol");
    goto error;
  }
  url += 5+3; /* Skip "RSC68://" */

  /* Get resource type. */
  for (i=0; 1; ++i) {
    int c = url[i] & 255;
    if (!c || c == '/') {
      protocol[i]=0;
      url += i + (c=='/');
      break;
    }
    protocol[i] = c;
    if (i >= sizeof(protocol)-1) {
      msg68_critical("rsc68: invalid RSC68 url; resource type too long '%s'",
                     url);
      goto error;
    }
  }

  /* Table should be initialized by proper library initialization. */
  /* rsc68_init_table(); */

  for (i=0; i<rsc68_last && strcmp68(rsc68_table[i].name, protocol); ++i)
    ;
  if (i >= rsc68_last) {
    msg68_critical("rsc68: invalid RSC68 url; invalid resource type '%s'",
                   protocol);
    goto error;
  }
  TRACE68(rsc68_cat,"rsc68: resource type #%d '%s'\n", i, protocol);
  is =  rsc68(i, url, mode, info);

error:
  TRACE68(rsc68_cat,"rsc68: open => [%s,'%s']\n",
          strok68(!is),istream68_filename(is));
  return is;
}

istream68_t * rsc68_open(rsc68_t type, const char *name, int mode,
                         rsc68_info_t * info)
{
  if (info) {
    info->type = rsc68_last;
  }
  if (!rsc68 || mode < 1 || mode > 2) {
    return 0;
  }
  return rsc68(type, name, mode, info);
}

int rsc68_init(void)
{
  int err = -1;

  if (init) {
    msg68_critical("rsc68: already initialized\n");
  } else {
    rsc68_cat =
      msg68_cat("rsc","resource access protocol",DEBUG_RSC68_O);

    rsc68 = default_open;
    rsc68_init_table();
    rsc68_set_share(FILE68_SHARED_PATH);
    rsc68_set_user(FILE68_USER_PATH);
    rsc68_set_music(FILE68_MUSIC_PATH);
    rsc68_set_remote_music(FILE68_RMUSIC_PATH);

    TRACE68(rsc68_cat,"rsc68: shared-data = '%s'\n",share_path);
    TRACE68(rsc68_cat,"rsc68: user_path   = '%s'\n",user_path);
    TRACE68(rsc68_cat,"rsc68: lmusic_path = '%s'\n",lmusic_path);
    TRACE68(rsc68_cat,"rsc68: rmusic_path = '%s'\n",rmusic_path);

    init = 1;
    err = 0;
  }
  return err;
}

void rsc68_shutdown(void)
{
  if (init) {
    /* destroy pathes. */
    rsc68_set_share(0);
    rsc68_set_user(0);
    rsc68_set_music(0);
    rsc68_set_remote_music(0);
    rsc68 = default_open;
    init  = 0;
  }
  TRACE68(rsc68_cat,"rsc68: *%s*\n","SHUTDOWN");
}

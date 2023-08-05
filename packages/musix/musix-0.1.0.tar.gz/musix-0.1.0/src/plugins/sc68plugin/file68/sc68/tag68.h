/**
 * @ingroup  file68_lib
 * @file     sc68/tag68.h
 * @author   Benjamin Gerard
 * @date     2011-10-03
 * @brief    Metatags definition header file.
 *
 */

/* Copyright (C) 1998-2011 Benjamin Gerard */

#ifndef _FILE68_TAG68_H_
#define _FILE68_TAG68_H_

/**
 * @addtogroup   file68_lib
 * @{
 */

/**
 * SC68 meta data.
 */
typedef struct {
  char * key;                     /**< Tag name.  */
  char * val;                     /**< Tag value. */
} tag68_t;

enum {
  TAG68_ID_TITLE  = 0,                  /**< Album or track name.      */
  TAG68_ID_ARTIST,                      /**< Artist full name.         */
  TAG68_ID_GENRE,                       /**< Genre is for tracks only. */
  TAG68_ID_CUSTOM,                      /**< First custom metatag.     */
  TAG68_ID_ALBUM  = TAG68_ID_TITLE,
  TAG68_ID_AUTHOR = TAG68_ID_ARTIST,
  TAG68_ID_FORMAT = TAG68_ID_GENRE,     /**< FORMAT is for album only. */
  TAG68_ID_MAX    = 12                  /**< Maximum number of tag.    */
};

/** tag set type. */
typedef union {
  tag68_t array[TAG68_ID_MAX];    /**< Tags indexed by TAG68_ID enum. */
  struct {
    tag68_t title;                /**< Static tag for title/album.   */
    tag68_t artist;               /**< Static tag for artist.        */
    tag68_t genre;                /**< Static tag for genre/format   */
    /** Other custom tags. */
    tag68_t custom[TAG68_ID_MAX-TAG68_ID_CUSTOM];
  } tag;
} tagset68_t;

/* Fixed position tags */
#define TAG68_TITLE      "title"
#define TAG68_ARTIST     "artist"
#define TAG68_GENRE      "genre"
#define TAG68_FORMAT     "format"

/* Well-known Custom tags */
#define TAG68_COMMENT    "comment"
#define TAG68_COPYRIGHT  "copyright"
#define TAG68_IMAGE      "image"
#define TAG68_RATE       "rate"
#define TAG68_REPLAY     "replay"
#define TAG68_RIPPER     "ripper"
#define TAG68_YEAR       "year"
#define TAG68_AKA        "aka"
#define TAG68_COMPOSER   "composer"
#define TAG68_CONVERTER  "converter"

/* Aliases tags */
#define TAG68_ALBUM      TAG68_TITLE
#define TAG68_AUTHOR     TAG68_ARTIST
#define TAG68_ALIAS      TAG68_TAG

/**
 * @}
 */

/**
 * @}
 */

#endif /* #ifndef _FILE68_TAG68_H_ */

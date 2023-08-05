/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *   Mupen64plus - game_controller.c                                       *
 *   Mupen64Plus homepage: http://code.google.com/p/mupen64plus/           *
 *   Copyright (C) 2014 Bobby Smiles                                       *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.          *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#include "usf/usf.h"

#include "game_controller.h"
#include "pif.h"

#include "api/m64p_types.h"
#include "api/callbacks.h"

#ifdef COMPARE_CORE
#include "api/debugger.h"
#endif

#include <string.h>


static uint8_t pak_data_crc(const uint8_t* data)
{
    size_t i;
    uint8_t crc = 0;

    for(i = 0; i <= 0x20; ++i)
    {
        int mask;
        for (mask = 0x80; mask >= 1; mask >>= 1)
        {
            uint8_t xor_tap = (crc & 0x80) ? 0x85 : 0x00;
            crc <<= 1;
            if (i != 0x20 && (data[i] & mask)) crc |= 1;
            crc ^= xor_tap;
        }
    }
    return crc;
}


static void read_controller_read_buttons(struct game_controller* cont, uint8_t* cmd)
{
}


static void controller_status_command(struct game_controller* cont, uint8_t* cmd)
{
    int connected = 0;

    if (cmd[1] & 0x80)
        return;

    if (!connected)
    {
        cmd[1] |= 0x80;
        return;
    }
}

static void controller_read_buttons_command(struct game_controller* cont, uint8_t* cmd)
{
    enum pak_type pak;
    int connected = 0;

    if (!connected)
        cmd[1] |= 0x80;
}

static void controller_read_pak_command(struct game_controller* cont, uint8_t* cmd)
{
    int connected = 0;

    if (!connected)
    {
        cmd[1] |= 0x80;
        return;
    }
}

static void controller_write_pak_command(struct game_controller* cont, uint8_t* cmd)
{
    int connected = 0;

    if (!connected)
    {
        cmd[1] |= 0x80;
        return;
    }
}


int game_controller_is_connected(struct game_controller* cont, enum pak_type* pak)
{
    return 0;
}

uint32_t game_controller_get_input(struct game_controller* cont)
{
    return 0;
}


void process_controller_command(struct game_controller* cont, uint8_t* cmd)
{
    switch (cmd[2])
    {
    case PIF_CMD_STATUS:
    case PIF_CMD_RESET:
        controller_status_command(cont, cmd); break;
    case PIF_CMD_CONTROLLER_READ:
        controller_read_buttons_command(cont, cmd); break;
    case PIF_CMD_PAK_READ:
        controller_read_pak_command(cont, cmd); break;
    case PIF_CMD_PAK_WRITE:
        controller_write_pak_command(cont, cmd); break;
        break;
    }
}

void read_controller(struct game_controller* cont, uint8_t* cmd)
{
    switch (cmd[2])
    {
    case PIF_CMD_CONTROLLER_READ: read_controller_read_buttons(cont, cmd); break;
    }
}


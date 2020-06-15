/** @copyright (C) 2020,  Gavin J Stark.  All rights reserved.
 *
 * @copyright
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0.
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 * @file   prng.h
 * @brief  Header file for pseudo-random number generation
 *
 */

/*a Includes
 */

/*a Types */
/*t t_prng_data */
typedef struct {
    bit valid;
    bit data;
} t_prng_data;

/*t t_prng_config */
typedef struct {
    bit enable;
    bit[3] min_valid;
    bit    seed_request;
} t_prng_config;

/*t t_prng_status */
typedef struct {
    bit seed_complete;
    t_prng_data data;
} t_prng_status;

/*t t_prng_whiteness_control
 */
typedef struct {
    bit      request;
    bit[16]  control "Control broken out by the whiteness monitor";
    bit[32]  run_length;
} t_prng_whiteness_control;

/*t t_prng_whiteness_result
 */
typedef struct {
    bit ack;
    bit valid;
    bit[64] data;
} t_prng_whiteness_result;

/*a Modules */
/*m prng */
extern module prng( clock clk         "System clock",
             input bit reset_n "Active low reset",
             input bit entropy_in "Entropy from external entropy sources",
             input t_prng_config prng_config "Configuration of PRNG",
             output t_prng_status prng_status "Status of PRNG including data"
    )
{
    timing to   rising clock clk entropy_in;
    timing to   rising clock clk prng_config;
    timing from rising clock clk prng_status;
}

/*m prng_whiteness_monitor */
extern module prng_whiteness_monitor( clock clk         "System clock",
                                      input bit reset_n "Active low reset",
                                      input t_prng_data data_in "Data from PRNG",
                                      input t_prng_whiteness_control whiteness_control "Control (enable, type etc) of whiteness monitor",
                                      output t_prng_whiteness_result whiteness_result  "Results from whiteness monitor,"
    )
{
    timing to   rising clock clk data_in;
    timing to   rising clock clk whiteness_control;
    timing from rising clock clk whiteness_result;
}



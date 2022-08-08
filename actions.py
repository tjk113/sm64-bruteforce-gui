# taken from 'Actions.lua' in the InputDirection lua
actions = {
	"uninitialized": 0x00000000,
	"idle": 0x0C400201,
	"start sleeping": 0x0C400202,
	"sleeping": 0x0C000203,
	"waking up": 0x0C000204,
	"panting": 0x0C400205,
	"hold panting (unused)": 0x08000206,
	"hold idle": 0x08000207,
	"hold heavy idle": 0x08000208,
	"standing against wall": 0x0C400209,
	"coughing": 0x0C40020A,
	"shivering": 0x0C40020B,
	"in quicksand": 0x0002020D,
	"unknown 2020E": 0x0002020E,
	"crouching": 0x0C008220,
	"start crouching": 0x0C008221,
	"stop crouching": 0x0C008222,
	"start crawling": 0x0C008223,
	"stop crawling": 0x0C008224,
	"slide kick slide stop": 0x08000225,
	"shockwave bounce": 0x00020226,
	"first person": 0x0C000227,
	"backflip land stop": 0x0800022F,
	"jump land stop": 0x0C000230,
	"double jump land stop": 0x0C000231,
	"freefall land stop": 0x0C000232,
	"side flip land stop": 0x0C000233,
	"hold jump land stop": 0x08000234,
	"hold freefall land stop": 0x08000235,
	"air throw land": 0x80000A36,
	"twirl land": 0x18800238,
	"lava boost land": 0x08000239,
	"triple jump land stop": 0x0800023A,
	"long jump land stop": 0x0800023B,
	"ground pound land": 0x0080023C,
	"braking stop": 0x0C00023D,
	"butt slide stop": 0x0C00023E,
	"hold butt slide stop": 0x0800043F,
	"walking": 0x04000440,
	"hold walking": 0x00000442,
	"turning around": 0x00000443,
	"finish turning around": 0x00000444,
	"braking": 0x04000445,
	"riding shell ground": 0x20810446,
	"hold heavy walking": 0x00000447,
	"crawling": 0x04008448,
	"burning ground": 0x00020449,
	"decelerating": 0x0400044A,
	"hold decelerating": 0x0000044B,
	"begin sliding": 0x00000050,
	"hold begin sliding": 0x00000051,
	"butt slide": 0x00840452,
	"stomach slide": 0x008C0453,
	"hold butt slide": 0x00840454,
	"hold stomach slide": 0x008C0455,
	"dive slide": 0x00880456,
	"move punching": 0x00800457,
	"crouch slide": 0x04808459,
	"slide kick slide": 0x0080045A,
	"hard backward ground kb": 0x00020460,
	"hard forward ground kb": 0x00020461,
	"backward ground kb": 0x00020462,
	"forward ground kb": 0x00020463,
	"soft backward ground kb": 0x00020464,
	"soft forward ground kb": 0x00020465,
	"ground bonk": 0x00020466,
	"death exit land": 0x00020467,
	"jump land": 0x04000470,
	"freefall land": 0x04000471,
	"double jump land": 0x04000472,
	"side flip land": 0x04000473,
	"hold jump land": 0x00000474,
	"hold freefall land": 0x00000475,
	"quicksand jump land": 0x00000476,
	"hold quicksand jump land": 0x00000477,
	"triple jump land": 0x04000478,
	"long jump land": 0x00000479,
	"backflip land": 0x0400047A,
	"jump": 0x03000880,
	"double jump": 0x03000881,
	"triple jump": 0x01000882,
	"backflip": 0x01000883,
	"steep jump": 0x03000885,
	"wall kick air": 0x03000886,
	"side flip": 0x01000887,
	"long jump": 0x03000888,
	"water jump": 0x01000889,
	"dive": 0x0188088A,
	"freefall": 0x0100088C,
	"top of pole jump": 0x0300088D,
	"butt slide air": 0x0300088E,
	"flying triple jump": 0x03000894,
	"shot from cannon": 0x00880898,
	"flying": 0x10880899,
	"riding shell jump": 0x0281089A,
	"riding shell fall": 0x0081089B,
	"vertical wind": 0x1008089C,
	"hold jump": 0x030008A0,
	"hold freefall": 0x010008A1,
	"hold butt slide air": 0x010008A2,
	"hold water jump": 0x010008A3,
	"twirling": 0x108008A4,
	"forward rollout": 0x010008A6,
	"air hit wall": 0x000008A7,
	"riding hoot": 0x000004A8,
	"ground pound": 0x008008A9,
	"slide kick": 0x018008AA,
	"air throw": 0x830008AB,
	"jump kick": 0x018008AC,
	"backward rollout": 0x010008AD,
	"crazy box bounce": 0x000008AE,
	"special triple jump": 0x030008AF,
	"backward air kb": 0x010208B0,
	"forward air kb": 0x010208B1,
	"hard forward air kb": 0x010208B2,
	"hard backward air kb": 0x010208B3,
	"burning jump": 0x010208B4,
	"burning fall": 0x010208B5,
	"soft bonk": 0x010208B6,
	"lava boost": 0x010208B7,
	"getting blown": 0x010208B8,
	"thrown forward": 0x010208BD,
	"thrown backward": 0x010208BE,
	"water idle": 0x380022C0,
	"hold water idle": 0x380022C1,
	"water action end": 0x300022C2,
	"hold water action end": 0x300022C3,
	"drowning": 0x300032C4,
	"backward water kb": 0x300222C5,
	"forward water kb": 0x300222C6,
	"water death": 0x300032C7,
	"water shocked": 0x300222C8,
	"breaststroke": 0x300024D0,
	"swimming end": 0x300024D1,
	"flutter kick": 0x300024D2,
	"hold breaststroke": 0x300024D3,
	"hold swimming end": 0x300024D4,
	"hold flutter kick": 0x300024D5,
	"water shell swimming": 0x300024D6,
	"water throw": 0x300024E0,
	"water punch": 0x300024E1,
	"water plunge": 0x300022E2,
	"caught in whirlpool": 0x300222E3,
	"metal water standing": 0x080042F0,
	"hold metal water standing": 0x080042F1,
	"metal water walking": 0x000044F2,
	"hold metal water walking": 0x000044F3,
	"metal water falling": 0x000042F4,
	"hold metal water falling": 0x000042F5,
	"metal water fall land": 0x000042F6,
	"hold metal water fall land": 0x000042F7,
	"metal water jump": 0x000044F8,
	"hold metal water jump": 0x000044F9,
	"metal water jump land": 0x000044FA,
	"hold metal water jump land": 0x000044FB,
	"disappeared": 0x00001300,
	"intro cutscene": 0x04001301,
	"star dance exit": 0x00001302,
	"star dance water": 0x00001303,
	"fall after star grab": 0x00001904,
	"reading automatic dialog": 0x20001305,
	"reading npc dialog": 0x20001306,
	"star dance no exit": 0x00001307,
	"reading sign": 0x00001308,
	"grand star cutscene": 0x00001909,
	"waiting for dialog": 0x0000130A,
	"debug free move": 0x0000130F,
	"standing death": 0x00021311,
	"quicksand death": 0x00021312,
	"electrocution": 0x00021313,
	"suffocation": 0x00021314,
	"death on stomach": 0x00021315,
	"death on back": 0x00021316,
	"eaten by bubba": 0x00021317,
	"peach cutscene": 0x00001918,
	"credits": 0x00001319,
	"waving": 0x0000131A,
	"pulling door": 0x00001320,
	"pushing door": 0x00001321,
	"warp door spawn": 0x00001322,
	"emerge from pipe": 0x00001923,
	"spawn spin airborne": 0x00001924,
	"spawn spin landing": 0x00001325,
	"exit airborne": 0x00001926,
	"exit land save dialog": 0x00001327,
	"death exit": 0x00001928,
	"death exit (unused)": 0x00001929,
	"falling death exit": 0x0000192A,
	"special exit airborne": 0x0000192B,
	"special death exit": 0x0000192C,
	"falling exit airborne": 0x0000192D,
	"unlocking key door": 0x0000132E,
	"unlocking star door": 0x0000132F,
	"entering star door": 0x00001331,
	"spawn no spin airborne": 0x00001932,
	"spawn no spin landing": 0x00001333,
	"bbh enter jump": 0x00001934,
	"bbh enter spin": 0x00001535,
	"teleport fade out": 0x00001336,
	"teleport fade in": 0x00001337,
	"shocked": 0x00020338,
	"squished": 0x00020339,
	"head stuck in ground": 0x0002033A,
	"butt stuck in ground": 0x0002033B,
	"feet stuck in ground": 0x0002033C,
	"putting on cap": 0x0000133D,
	"holding pole": 0x08100340,
	"grab pole slow": 0x00100341,
	"grab pole fast": 0x00100342,
	"climbing pole": 0x00100343,
	"top of pole transition": 0x00100344,
	"top of pole": 0x00100345,
	"start hanging": 0x08200348,
	"hanging": 0x00200349,
	"hang moving": 0x0020054A,
	"ledge grab": 0x0800034B,
	"ledge climb slow 1": 0x0000054C,
	"ledge climb slow 2": 0x0000054D,
	"ledge climb down": 0x0000054E,
	"ledge climb fast": 0x0000054F,
	"grabbed": 0x00020370,
	"in cannon": 0x00001371,
	"tornado twirling": 0x10020372,
	"punching": 0x00800380,
	"picking up": 0x00000383,
	"dive picking up": 0x00000385,
	"stomach slide stop": 0x00000386,
	"placing down": 0x00000387,
	"throwing": 0x80000588,
	"heavy throw": 0x80000589,
	"picking up bowser": 0x00000390,
	"holding bowser": 0x00000391,
	"releasing bowser": 0x00000392
}
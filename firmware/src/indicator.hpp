# ifndef indicator_hpp
# define indicator_hpp

# define SIGNATURE "lite\n"

# define PIXELS 8
# define PIN_NEOPIX 2

# define PIN_BUTTON1 8
# define PIN_BUTTON2 12
# define PIN_GND1 6
# define PIN_GND2 10s

# define POS_NONE (255)

# define MOD_IDLE (0)
# define MOD_BRITE (1)
# define MOD_POS (2)
# define MOD_DATA (3)

inline bool procChar();
inline void procMode();
void clear(int r,int g,int b);

# endif

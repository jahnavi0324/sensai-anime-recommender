const FRICTION = 0.86; // 0.98 for yellow text effect, 0.86 for black text effect
const MOVE_SPEED = 0.1; // 0.2 for yellow, 0.1 for black

export class Particle {
    constructor(pos, texture) {
        this.sprite = new PIXI.Sprite(texture);
        this.sprite.scale.set(0.2);
        this.sprite.tint = 0x000000;
        // keep above line for black text effect, comment for yellow text effect

        this.savedX = pos.x;
        this.savedY = pos.y;
        this.x = pos.x;
        this.y = pos.y;
        this.sprite.x = this.x;
        this.sprite.y = this.y;
        this.vx = 0;
        this.vy = 0;
        this.radius = 10;
    }
    
    draw() {
        this.vx += (this.savedX - this.x) * MOVE_SPEED; //this.x for yellow text, this.vx for black text
        this.vy += (this.savedY - this.y) * MOVE_SPEED; //this.y for yellow text, this.vy for black text

        this.vx *= FRICTION;
        this.vy *= FRICTION;

        this.x += this.vx;
        this.y += this.vy;

        this.sprite.x = this.x;
        this.sprite.y = this.y;
    }

}
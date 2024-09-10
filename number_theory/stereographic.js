import * as THREE from "./three.module.js";
import { OrbitControls } from "./orbit_controls.js";

// three js stuff

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls( camera, renderer.domElement );
controls.enableDamping = true;
controls.enablePan = false;

camera.position.z = 2;
controls.update();

// lighting

const light1 = new THREE.PointLight(0xffffff);
light1.position.set(1, 2, 1);
scene.add(light1);

const light2 = new THREE.PointLight(0xffffff);
light2.position.set(0, 0, 3);
scene.add(light2);

const light3 = new THREE.AmbientLight(0x222222);
scene.add(light3);

// riemann sphere

const riemann_sphere_geo = new THREE.SphereGeometry(1, 64, 32);
const riemann_sphere_mat = new THREE.MeshBasicMaterial({
    color: 0xffffaa,
    transparent: true,
    opacity: 0.5,
    
});
const riemann_sphere = new THREE.Mesh(riemann_sphere_geo, riemann_sphere_mat);
scene.add(riemann_sphere);



const equator_points = [];
for (let i = 0; i <= 100; i++) {
    const scale = 1.01;
    const angle = 2 * Math.PI * i / 100;
    const x = scale * Math.cos(angle);
    const z = scale * Math.sin(angle);
    equator_points.push( new THREE.Vector3(x, 0, z) );
}
const equator_mat = new THREE.LineBasicMaterial({
    color: 0xff0000,
});
const equator_geo = new THREE.BufferGeometry().setFromPoints( equator_points );
const equator = new THREE.Line(equator_geo, equator_mat);
scene.add(equator);

function project_to_riemann_sphere(a, b) {

    const scale = 1.01;
    
    const x = 2 * a / (1 + a*a + b*b);
    const y = 2 * b / (1 + a*a + b*b);
    const z = (a*a + b*b - 1) / (1 + a*a + b*b);
    
    return new THREE.Vector3(scale*x, scale*z, scale*y);
}

function expi(theta) {
    return [Math.cos(theta), Math.sin(theta)];
}

let t = 1;

const sum_points = [[0, 0]];

for (let n = 1; n <= 1001; n++) {

    const term = expi(2 * Math.PI / n * t);
    console.log(`${term[0]} + i${term[1]}`);
    const prev_sum = sum_points[sum_points.length - 1];
    const sum = [prev_sum[0] + term[0], prev_sum[1] + term[1]];
    
    sum_points.push(sum);
}

const projected_sum_points = sum_points.map(p => { return project_to_riemann_sphere(p[0], p[1]); });
console.log(projected_sum_points);
const sum_mat = new THREE.LineBasicMaterial({
    color: 0x0000ff,
});
const sum_geo = new THREE.BufferGeometry().setFromPoints( projected_sum_points );
const sum_line = new THREE.Line(sum_geo, sum_mat);
scene.add(sum_line);

function render() {
    requestAnimationFrame(render);

    controls.update();
    
    renderer.render(scene, camera);
}

render();

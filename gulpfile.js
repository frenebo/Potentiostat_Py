// var gulp = require("gulp");
import gulp from "gulp";
import tslint from "gulp-tslint";
import ts from "gulp-typescript";
// var ts = require("gulp-typescript");
// var del = require("del");
import { deleteAsync } from "del";
// var gulpTslint = require("gulp-tslint");
// var tslint = require("tslint");

gulp.task("clean", () => deleteAsync(["website/build"]));

gulp.task("copy", () => gulp.src(["website/source/**/*", "!website/source/**/*.ts"]).pipe(gulp.dest("website/build")));

// gulp.task("copy_pixi", () => {
//   return gulp.src(["node_modules/pixi.js/dist/pixi.js"]).pipe(
//     gulp.dest("src/website/build/deps/pixi"),
//   );
// });

// gulp.task("copy_socketio", () => {
//   return gulp.src(["node_modules/socket.io-client/dist/socket.io.js"]).pipe(
//     gulp.dest("src/website/build/deps/socketio"),
//   );
// });

gulp.task("ts", function() {
  var client_project = ts.createProject('website/tsconfig.json');
  return gulp.src(["website/source/**/*.ts", "node_modules/types/@types/**/*.d.ts"])
    .pipe(client_project()).js
    .pipe(gulp.dest("website/build"));
});

gulp.task("build", gulp.series(
  "clean",
  "ts",
  "copy",
));

gulp.task("tslint", function() {
  var program = tslint.Linter.createProgram("./website/tsconfig.json");

  return gulp.src(["client/app/**/*.ts"])
    .pipe(tslint({ program: program }))
    .pipe(tslint.report({
      configuration: {},
      rulesDirectory: null,
      emitError: true,
      reportLimit: 0,
      summarizeFailureOutput: true,
    }));
});